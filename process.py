# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:56:06 2021

@author: Simona
"""
import os, sys
import opts as opt
import seaborn as sns
import postprocess

path = opt.path

#Change dir to the analysis
os.chdir(path)

#Makes directories in a root directory and creates variables
postprocess.makeDirs(path)

#Create variables used by the methods
seg_out = opt.path + 'seg_out/'
originals_path = path + 'originals/'
images_path = path + 'cropped/'
masks_edgefree_path = path + 'edgefree/'
results_path = path + 'results/'
masks_path = path + 'seg_out/masks/'
outlines_path = path + 'outlines/'

#1. Cropping original images
if opt.crop == True:
    postprocess.crop(originals_path, images_path, opt.width, opt.height, opt.new_width, opt.new_height)

#Run the segmentation
import segmentation

#2. Remove edge touching objects from the masks
postprocess.remove_edges(masks_path, masks_edgefree_path)

#Save outlines and look how it looks like in folder outlines
postprocess.outline(images_path, masks_path, outlines_path)

#Measure properties and save them to a variable
results = postprocess.measure_img(images_path, masks_edgefree_path, results_path, opt.scale)

#Measure growth ratio and save results
if opt.growthratio == True:
    growth = postprocess.growthrate(opt.area_threshold, results)
    growth.to_csv(results_path + 'growth_rate.csv')

#Quick plot check for distribution of values
plot = sns.catplot(x="filename", y="mean_intensity", kind="violin", inner=None, data=results)
sns.swarmplot(x="filename", y="mean_intensity", color="k", size=1, data=results)

plot.set_xticklabels(rotation=30)
plot.savefig(results_path + 'plot.png', dpi=300)
