# Yeast fluorescent protein intensity pipeline for relative expression levels of proteins in yeast cells

This is a tool for processing of fluorescent microscopy images of yeast cells. This tool is based on neural network image segmentation from Alex Xijielu - YeastSpotter (https://github.com/alexxijielu/yeast_segmentation). It extends the tool to enable extract data from single cells, such as mean pixel intensity and area.
It enables for user-friendly high-throughput data extraction (mean intensity and area) coupled with precise yeast segmentation by YeastSpotter. It can be used to estimate differences between relative protein expression from fluorescent images.

<h2>STEPS:</h2>
1. Clone the repository https://github.com/alexxijielu/yeast_segmentation and setup its dependencies to your environment, including downloading the weights
2. Replace the opts.py file with an opts.py file in this repository
1. Setup a directory where will take place your analysis (i.e. '/home/analysis/').
2. In this directory, create a directory called 'originals' with your original images('/home/analysis/originals/')
4. In the directory with the scripts
3. Open file opts.py and specify path to the directory with the scripts (i.e. '/home/scripts/') and path to the directory with your analysis ('/home/analysis/').
4. in the opts.py file, specify parameters for processing and segmentation
5. Run process.py file


<h2>This pipeline will:</h2>

1. Crop your images to desired size
2. Segment individual yeast cells (YeastSpotter) and output masks '/analysis/seg_out/masks/'
3. Match your images with masks for control of the segmentation output and save them to '/analysis/outlines/'
4. Removes edge touching objects from the mask
5. Measures the specified properties (see postprocess.py)
6. Plot the mean intensities per sample (violin plot default)
8. Convert the area of the cells to square microns, and categorize them big/small to see the growth ratio (small cells are after division)
7. Save results in '/home/analysis/results/' (csv tables, png plot)

<h2>Example result plot</h2>
