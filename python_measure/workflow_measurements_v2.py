# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:26:36 2020

@author: Simona
"""
from skimage.color import label2rgb, rgb2gray
from skimage.segmentation import clear_border
from skimage import measure, io, img_as_ubyte
import pandas as pd
import numpy as np
import cv2
import os
import glob
import matplotlib.pyplot as plt
from PIL import Image
import skimage.morphology
import skimage.exposure
import os.path,sys
import seaborn as sns


#Define variables and filepaths
home = r'/home/simona/'
os.chdir(home)

#Folder where I will do analysis
path = 'Documents/simona/lab/micro/analysis/exo_ng_30C/'

#make directories for analysis
os.mkdir(path + 'seg_out')
os.mkdir(path + 'originals')
os.mkdir(path + 'cropped')
os.mkdir(path + 'edgefree')
os.mkdir(path + 'results')
os.mkdir(path + 'outlines')

seg_out = path + 'seg_out/'
originals_path = path + 'originals'
images_path = path + 'cropped/'
masks_edgefree_path = path + 'edgefree/'
results_path = path + 'results/'
masks_path = path + 'seg_out/masks/'
outlines_path = path + 'outlines/'



#1. Cropping original images
# Get values for the crop function:

#Here comes width and heigth of my pictures originals and desired size
width = 2048
height = 2048

new_width = 1024
new_height = 1024


left = (width - new_width)/2
top = (height - new_height)/2
right = (width + new_width)/2
bottom = (height + new_height)/2


def crop(originals_path, images_path):
    
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

crop(originals_path, images_path)
#2. Define function that will take all masks outputted from the NN and removes the edge touching objects

def remove_edges(masks_path, masks_edgefree_path):
    
    masks_list = os.listdir(masks_path)
    
    for mask in masks_list:
        fullpath_mask = os.path.join(masks_path, mask)
        
        if os.path.isfile(fullpath_mask):
            seg = np.array(Image.open(fullpath_mask))
            edge_touching_removed = clear_border(seg)
            print('Edge touching objects for ' + mask + ' were removed')
            edge_touching_removed = edge_touching_removed.astype(np.int64)
            np.save(masks_edgefree_path + mask + 'numpy.npy', edge_touching_removed)
            

#Get alist of the edge free masks saved as np arrs


remove_edges(masks_path, masks_edgefree_path)



def outline(images_path, masks_path, outlines_path):
    
    masks_list = os.listdir(masks_path)
    masks_list = sorted(masks_list)
    images_list = os.listdir(images_path)
    images_list = sorted(images_list)


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

outline(images_path, masks_path, outlines_path)

results = []

def measure_properties(images_path, masks_edgefree_path):
    
    masks_edgefree_list = os.listdir(masks_edgefree_path)
    masks_edgefree_list = sorted(masks_edgefree_list)
    images_list = os.listdir(images_path)
    images_list = sorted(images_list)

    
    for i, image in enumerate(images_list):
        fullpath_image = os.path.join(images_path, image)
        fullpath_mask = os.path.join(masks_edgefree_path, masks_edgefree_list[i])
        
        if os.path.isfile(fullpath_image):
            img = io.imread(fullpath_image)
            print('loading image' + fullpath_image)
            mask = np.load(fullpath_mask)
            print('loading mask' + fullpath_mask)
            props = measure.regionprops_table(mask, img, properties=['label','area', 'equivalent_diameter', 'mean_intensity', 'max_intensity'])
            props = pd.DataFrame(props)
            props = props.assign(filename=image[0:7])
            print(props)
            results.append(props)

measure_properties(images_path, masks_edgefree_path)

results_all = pd.concat(results)
scale = 0.0645
results_all['area_sq_microns'] = results_all['area'] * (scale**2)
results_all.to_csv(results_path + 'results.csv')


 images_list = os.listdir(images_path)
sorting = sorted(images_list)
 masks_edgefree_list = os.listdir(masks_edgefree_path)






#Incorporate the small/big cell ratio
ratios = []

def small_cells(area_threshold, results):
    small = results.groupby('filename')['area'].apply(lambda x: (x<area_threshold).sum()).reset_index(name='count')
    
    return small
    
def big_cells(area_threshold, results):
    big = results.groupby('filename')['area'].apply(lambda x: (x>area_threshold).sum()).reset_index(name='count')
    return big

area_threshold=2000

small = small_cells(area_threshold, results_all)
big = big_cells(area_threshold, results_all)

ratio = pd.DataFrame((small['count']/big['count'])*100)
ratio['filename'] = small['filename']

summary = results_all.groupby('filename').mean()



#Plotting
fig_dims = (10, 10)
fig, ax = plt.subplots(figsize=fig_dims)
g = sns.boxplot(x="filename", y="mean_intensity", ax=ax, data=results_all)
sns.swarmplot(x="filename", y="mean_intensity", color="k", size=0.5, data=results_all)
g.set(xticks(range(len(summary))) # <--- set the ticks first
g.set(xticks(['GFP_96wp_30C','GFP_ring_30C','GFP_ring_18C','NG_96wp_30C','NG_ring_30C','NG_ring_18C']))


List1 = os.listdir(path + 'brightfield')
List2 = os.listdir(path + 'originals')
newList2 = []
newList = []

for i in List2:
    newList2.append(i.split('_')[0])
    
from collections import Counter
c2 = Counter(newList2)
    
check =  all(item in List1 for item in List2)


#TukeyHSD
from statsmodels.stats.multicomp import MultiComparison
mod = MultiComparison(results_all['mean_intensity'], results_all['filename'])
results_hsd = mod.tukeyhsd()
result_hsd = results_hsd.plot_simultaneous()
