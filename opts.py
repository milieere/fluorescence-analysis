##### CHANGE THE PARAMETERS HERE #####################

#Path to the scripts
path_scripts = '/home/scripts/'

#Path to the analysis folder
path = '/home/analysis/'

#######################################

######### MODIFY PROCESSING OPTIONS HERE #########################

#If you want to crop images, set crop to True, otherwise False
crop = True

#Set original width and height and desired ones (new_width, new_height)
width = 2048
height = 2048
new_width = 800
new_height = 500

#If you want to do the growth rate of small/big cells set growthratio to True
growthratio = True

#Set the threshold (in square microns) dividing cells into two groups: small and big
area_threshold = 2

#Set scale for computing cell area in square microns (size of pixel in microns)
scale = 0.0645

################################################################


################## OPTIONS OF SEGMENTATION ###################
# Set to true to rescale the input images to reduce segmentation time
rescale = False
scale_factor = 2          # Factor to downsize images by if rescale is True

# Set to true to save preprocessed images as input to neural network (useful for debugging)
save_preprocessed = False

# Set to true to save a compressed RLE version of the masks for sharing
save_compressed = False

# Set to true to save the full masks
save_masks = True

# Set to true to have the neural network print out its segmentation progress as it proceeds
verbose = True

# Set to true to output ImageJ-compatible masks
output_imagej = False
##############################################################

#Append the script path to the system path
import sys
sys.path.append(path_scripts)

# Input directory of images to be segmented
if crop == True:
    input_directory = path + 'cropped/'
else:
    input_directory = path + 'originals/'

# Output directory to save masks to
output_directory = path + 'seg_out/'
