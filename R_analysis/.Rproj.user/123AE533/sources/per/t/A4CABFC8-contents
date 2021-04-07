library(dplyr)
library(ggplot2)


measurements <- read.csv(file='/home/simona/Documents/simona/lab/micro/analysis/gfp_ng_30C_18C/results/results.csv', header=TRUE, sep=',', na.strings='NA')
measurements <- measurements %>% group_by(sample)
summarise(measurements)

data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

summary <- data_summary(measurements, varname="mean_intensity", 
                               groupnames='filename')
# Convert dose to a factor variable
summary$sample=as.factor(summary$sample)
head(df2)

plot_ratios <- ggplot(data=total, mapping=aes(x=Filename, y=ratio, fill=Filename)) +
  geom_point(color="black", size=2, alpha=0.25) +
  geom_boxplot(width = 0.5, alpha = 0.6, color="black")+
  #scale_x_discrete(labels=c('GFP_96wp_30C','GFP_ring_30C','GFP_ring_18C','NG_96wp_30C','NG_ring_30C','NG_ring_18C')) +
  scale_fill_manual(values=c('#692983', '#4B619F', '#068BAC', '#16ADAC', '#69C7A6', '#ABDAA6', '#E1E7B6', '#FFEED1')) +
  theme_minimal() + theme(
    legend.position="none",
    plot.title = element_text(size=12, hjust=0)) +
  # + geom_errorbar(data=summary_ratio, aes(ymin=ratio-sd, ymax=ratio+sd), width=.4, position=position_dodge(.9)) 
  ggtitle("% of intensity in exocytic events") +   theme(plot.title = element_text(hjust = 0.5))

plot_ratios
´
  