#Check percentage of bright areas intensity from total intensity


#Load the intensity in segmented cells and bright areas
setwd('../../exo_96wp_e1000/results')

spots <- read.csv(file='results_spots.csv', header=TRUE, sep=',', na.strings='NA')
total <- read.csv(file='macro_results_improved.csv', header=TRUE, sep=',', na.strings='NA')

#Get rid of PGK1
spots <- spots[-grep("Pgk", spots$filename),]
total <- total[-grep(2.4119, total$ratio),]

#Slice the filenames
spots$filename <- substr(spots$filename,1,6)
total$Filename <- substr(total$Filename,1,6)

summary_total <- data_summary(total, varname="Mean", 
                                   groupnames='Filename')

#Get the ratio of spots/total*100 to see how many percent of int has the bright areas
total$ratio <- (spots$IntDen/total$IntDen)*100

#Summarize the ratios
summary_ratio <- data_summary(total, varname="ratio", 
                              groupnames='Filename')
