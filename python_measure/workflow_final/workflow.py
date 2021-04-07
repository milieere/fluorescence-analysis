# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:26:36 2020

@author: Simona


"""
import os ,sys
import seaborn as sns

#Adding path to the methods directory (directory with this script and postprocess.py)
sys.path.append('discoscience/doctorate_upf/micro/analyses/python_script_postprocess/final/')

#Imports methods in a separate files, check postprocess.py to see the methods called
import postprocess

#Define a root folder, which contains two directories - originals
#and seg_out with otputted masks from YeastSpotter
path = r'C:\Users\Simona\Documents/discoscience/doctorate_upf/micro/analyses/test/'
os.chdir(path)

#Makes directories in a root directory and creates variables
postprocess.makeDirs(path)

#Create variables used by the methods
seg_out = path + 'seg_out/'
originals_path = path + 'originals/'
images_path = path + 'cropped/'
masks_edgefree_path = path + 'edgefree/'
results_path = path + 'results/'
masks_path = path + 'seg_out/masks/'
outlines_path = path + 'outlines/'

#1. Cropping original images
postprocess.crop(originals_path, images_path, 2048, 2048, 1024, 1024)

#2. Remove edge touching objects from the masks
postprocess.remove_edges(masks_path, masks_edgefree_path)

#Save outlines and look how it looks like in folder outlines
postprocess.outline(images_path, masks_path, outlines_path)

#Measure properties and save them to a variable
results = postprocess.measure_img(images_path, masks_edgefree_path, results_path, 0.0645)

#Measure growth ratio
growth = postprocess.growthrate(2000, results)

#Quick plot check for distribution of values
plot = sns.catplot(x="filename", y="mean_intensity", kind="violin", inner=None, data=results)
sns.swarmplot(x="filename", y="mean_intensity", color="k", size=0.5, data=results)
