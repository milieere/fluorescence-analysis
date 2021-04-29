# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 11:50:43 2021

@author: Simona
"""

from skimage.color import label2rgb, rgb2gray
from skimage.segmentation import clear_border
from skimage import measure, io, img_as_ubyte
import pandas as pd
import numpy as np
import cv2
import os, sys
import glob
import matplotlib.pyplot as plt
from PIL import Image
import skimage.morphology
import skimage.exposure
import seaborn as sns


def makeDirs(path):
    """
    makeDirs Creates directory hierarchy in the analysis folder. 
    
    :param path: Takes the path to the root folder with analysis created by user
    """
        #make directories for analysis
    if not os.path.exists(path + 'seg_out'):
        os.makedirs(path + 'seg_out')
    if not os.path.exists(path + 'cropped'):
        os.makedirs(path + 'cropped')
    if not os.path.exists(path + 'edgefree'):
        os.makedirs(path + 'edgefree')
    if not os.path.exists(path + 'results'):
        os.makedirs(path + 'results')
    if not os.path.exists(path + 'outlines'):
        os.makedirs(path + 'outlines')


def crop(originals_path, images_path, width, height, new_width, new_height):
    """
    crop Crops the images to desired new height and weight, center-crop.
    
    :param originals_path: Path to original images
    :param images_path: Path to output folder where the cropped imgs will be saved
    :param width: width of original
    :param height: height of original
    :param new_width: width after cropping
    :param new_height: height after cropping
    """
    
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    original_list = os.listdir(originals_path)
    
    for original in original_list:
        print(original)
        fullpath = os.path.join(originals_path, original) #corrected
        print(fullpath)
        
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(images_path)
            print('splitted', f)
            imCrop = im.crop((left, top, right, bottom)) #corrected
            imCrop.save(images_path + original + 'Cropped.tif', "tiff", quality=100)
            


def remove_edges(masks_path, masks_edgefree_path):
    """
    remove_edges Takes masks outputted by segmentation, and removes
    objects that are touching the edges.
    
    :param masks_path: Path to masks outputted by the segmentation algorithm
    :param masks_edgefree_path: Path to output folder where the edgefree masks will be saved
    """
    masks_list = os.listdir(masks_path)
    
    for mask in masks_list:
        fullpath_mask = os.path.join(masks_path, mask)
        
        if os.path.isfile(fullpath_mask):
            seg = np.array(Image.open(fullpath_mask))
            edge_touching_removed = clear_border(seg)
            print('Edge touching objects for ' + mask + ' were removed')
            edge_touching_removed = edge_touching_removed.astype(np.int64)
            np.save(masks_edgefree_path + mask + 'numpy.npy', edge_touching_removed)



def outline(images_path, masks_path, outlines_path):
    '''
    outline Cobines masks and segmented images for control of the segmentation precision.
    
    Parameters
    ----------
    images_path : Path to masks outputted by the segmentation algorithm
    masks_path :  Path to output folder where the edgefree masks will be saved.
    outlines_path : Path to the folder where outlined images will be saved.
    -------
    Saves the outlined images in the outlines_path.

    '''
    
    masks_list = sorted(os.listdir(masks_path))
    images_list = sorted(os.listdir(images_path))

    for i, img in enumerate(images_list):
        fullpath_image = os.path.join(images_path, img)
        fullpath_mask = os.path.join(masks_path, masks_list[i])
        print(fullpath_mask)
        
        if os.path.isfile(fullpath_image):
            image = np.array(Image.open(fullpath_image))
            image = skimage.exposure.rescale_intensity(image.astype(np.float32), out_range=(0, 1))
            image = np.round(image * 255).astype(np.uint8)

            if len(image.shape) == 3 and image.shape[2] == 3:
                pass
            else:
                image = np.expand_dims(image, axis=-1)
                image = np.tile(image, 3)

        seg = np.array(Image.open(fullpath_mask))
        outlines = np.zeros(seg.shape)

        for i in range(1, int(np.max(seg) + 1)):
            tmp = np.zeros(seg.shape)
            tmp[np.where(seg == i)] = 1
            tmp = tmp - skimage.morphology.binary_erosion(tmp)
            outlines += list(tmp)
            print('done')
        image_outlined = image.copy()
        image_outlined[outlines > 0] = (0, 255, 0)
        
        plt.imshow(image_outlined)

        im = Image.fromarray(image_outlined)
        im.save(outlines_path + img + "_outlined.png", "png", quality=100)





def measure_img(images_path, masks_edgefree_path, results_path, scale):
    '''
    measure_img Takes cropped images and edgefree masks and measures the area
    inside the masks. Default properties measured are:
        'area', 'equivalent_diameter', 'mean_intensity', 'max_intensity'
    Area in square micron will be deduced based on the scale.
    To add more parameters modify the variable props down in the for loop.
    Results will be saved in csv file.

    Parameters
    ----------
    images_path : Path to the images.
    masks_edgefree_path : Path to the edgefree masks.
    results_path : Folder to save csv file with results.
    scale : Size of micron in pixels.

    Returns results: dataframe with results
    -------
    TYPE
        DESCRIPTION.

    '''
    
    results = []
    
    def measure_properties():
        
        masks_edgefree_list = sorted(os.listdir(masks_edgefree_path))
        images_list = sorted(os.listdir(images_path))
        
        for i, image in enumerate(images_list):
            fullpath_image = os.path.join(images_path, image)
            fullpath_mask = os.path.join(masks_edgefree_path, masks_edgefree_list[i])
        
            if os.path.isfile(fullpath_image):
                img = io.imread(fullpath_image)
                print('loading image')
                mask = np.load(fullpath_mask)
                print('loading mask')
                props = measure.regionprops_table(mask, img, properties=['label','area', 'equivalent_diameter', 'mean_intensity', 'max_intensity'])
                props = pd.DataFrame(props)
                props = props.assign(filename=image.split('_')[0])
                print(props)
                results.append(props)
        
        return results
    
    measure_properties()
    results_all = pd.concat(results)
    results_all['area_sq_microns'] = results_all['area'] * (scale**2)
    results_all['total_intensity'] = results_all['area'] * results_all['mean_intensity']
    results_all.to_csv(results_path + 'results.csv')
    return results_all


def growthrate(area_threshold, results):
    '''
    Parameters
    ----------
    area_threshold : Number dividing cells into small and big categories
    results :  Dataframe with results recorder by measure_img
    -------
    Returns dataframe with ratio for each sample
    '''
    
    def smallCells():
        small = results.groupby('filename')['area'].apply(lambda x: (x<area_threshold).sum()).reset_index(name='count')
        return small
    
    def bigCells():
        big = results.groupby('filename')['area'].apply(lambda x: (x>area_threshold).sum()).reset_index(name='count')
        return big
    
    small = smallCells()
    big = bigCells()

    ratio = pd.DataFrame((small['count']/big['count'])*100)
    ratio.rename(columns={'count':'perc_small'}, inplace=True)
    ratio['filename'] = small['filename']
    return ratio
