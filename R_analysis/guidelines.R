#SCRIPT TO IDENTIFY CANDIDATES FROM RNA-SEQ DEG ANALYSIS, EXOCYST RELEVANT GENES

#Loading basic data
exo_core <- read.csv(file='exo_core.csv', header=TRUE, sep=',', na.strings='NA')
sc30_sc12 <- read.csv(file='sc30_sc12.csv', header=TRUE, sep=',', na.strings='NA')

#Identifying DEGs based on log2FoldChange cutoff (1)
library(dplyr)
DEG_down <- filter(sc30_sc12, log2FoldChange < -1)
DEG_down <- DEG_down %>% arrange(log2FoldChange)
write.csv(DEG_down, file='DEG_down.csv')

DEG_up <- filter(sc30_sc12, log2FoldChange > 1)
DEG_up <- DEG_up %>% arrange(desc(log2FoldChange))
write.csv(DEG_up, file='DEG_up.csv')

#Are there up/downregulated genes in the list of DEGs that belong to the exo core machinery?
DEG_down_exo <- filter(DEG_down, (DEG_down$gene %in% exo_core$code) == TRUE) #Just RHO3
raw_exocore <- filter(sc30_sc12, (sc30_sc12$ï..gene %in% exo_core$code) == TRUE) #Just SRO77
raw_exocore <-left_join(exo_core, raw_exocore, merge, by=c('code' = 'ï..gene'))


#Load all physical interactions of the DEGs
DEG_down_int <- read.csv(file='./DEGs_all/DEG_down_int.csv', header=FALSE, sep=',', na.strings='NA')
DEG_up_int <- read.csv(file='./DEGs_all/DEG_up_int.csv', header=FALSE, sep=',', na.strings='NA')

#See which of the have exo members as interactors - intersection
DEG_down_exo <- filter(DEG_down_int, (DEG_down_int$V10 %in% exo_core$code) == TRUE)
DEG_up_exo <- filter(DEG_up_int, (DEG_up_int$V10 %in% exo_core$code) == TRUE)

#The document has duplicates, remove them based on two columns (I want to retrieve every specific interaction just once)
DEG_down_exo_filtered <- filter(DEG_down_exo, duplicated(DEG_down_exo[,c('V3', 'V10')]) != TRUE)
DEG_up_exo_filtered <- filter(DEG_up_exo, duplicated(DEG_up_exo[,c('V3', 'V10')]) != TRUE)

#Append the expression values to the list
DEG_down_exo_filtered_joined<-left_join(DEG_down_exo_filtered, DEG_down, merge, by=c('V3' = 'gene'))
DEG_down_exo_filtered_joined <- DEG_down_exo_filtered_joined %>% arrange(log2FoldChange)

DEG_up_exo_filtered_joined<-left_join(DEG_up_exo_filtered, DEG_up, merge, by=c('V3' = 'gene'))
DEG_up_exo_filtered_joined <- DEG_up_exo_filtered_joined %>% arrange(desc(log2FoldChange))

write.csv(DEG_down_exo_filtered_joined, file='DEG_down_exo.csv')
write.csv(DEG_up_exo_filtered_joined, file='DEG_up_exo.csv')



# //////////////// NOW WE HAVE THE LISTS. 
# HOW TO RANK THE CONTENTS OF THE LIST NOW? BASED ON NO OF 
# INTERACTIONS AND INTERACTIONS WITH EXOCYST MACHINERY///////////////////


#retrieve list of all physical interactions of list members (DEG_down_exo, DEG_up_exo) and count how many interactors has each
# + count how many interactions have the candidates from the list with the exo machinery

DEG_down_exo_int <- read.csv(file='./DEGs_exo/DEG_down_exo_int.csv', header=FALSE, sep=',', na.strings='NA')
DEG_down_exo_int <- filter(DEG_down_exo_int, duplicated(DEG_down_exo_int[,c('V3', 'V10')]) != TRUE)

DEG_up_exo_int <- read.csv(file='./DEGs_exo/DEG_up_exo_int.csv', header=FALSE, sep=',', na.strings='NA')
DEG_up_exo_int <- filter(DEG_up_exo_int, duplicated(DEG_up_exo_int[,c('V3', 'V10')]) != TRUE)

DEG_down_exo_int_counts <- as.data.frame(table(DEG_down_exo_int$V3)) #Counts of all interactions of the candidates 
DEG_down_exo_int_counts$new <- table(DEG_down_exo_filtered_joined$V3)
DEG_down_exo_int_counts$ratio <- (DEG_down_exo_int_counts$new / DEG_down_exo_int_counts$Freq)
DEG_down_exo_int_counts <- DEG_down_exo_int_counts %>% arrange(desc(ratio))

DEG_down_exo_int_counts <- DEG_down_exo_int_counts %<>% mutate_if(is.factor,as.character) #transform the columns into characters depending on what type waefore, can find out with str()
DEG_down_exo_filtered_joined <- DEG_down_exo_filtered_joined %<>% mutate_if(is.factor,as.character)
DEG_down_exo_filtered_joined_sorted<-left_join(DEG_down_exo_filtered_joined, DEG_down_exo_int_counts, merge, by=c('V3' = 'Var1'))
DEG_down_exo_filtered_joined_sorted<- DEG_down_exo_filtered_joined_sorted %>% arrange(desc(ratio))
write.csv(DEG_down_exo_filtered_joined_sorted, file='DEG_down_candidates_sorted.csv')

DEG_up_exo_int_counts <- as.data.frame(table(DEG_up_exo_int$V3)) #Counts of all interactions of the candidates 
DEG_up_exo_int_counts$new <- table(DEG_up_exo_filtered_joined$V3)
DEG_up_exo_int_counts$ratio <- (DEG_up_exo_int_counts$new / DEG_up_exo_int_counts$Freq)
DEG_up_exo_int_counts <- DEG_up_exo_int_counts %>% arrange(desc(ratio))

DEG_up_exo_int_counts <- DEG_up_exo_int_counts %<>% mutate_if(is.numeric,as.character) #transform the columns into characters depending on what type waefore, can find out with str()
DEG_up_exo_filtered_joined <- DEG_up_exo_filtered_joined %<>% mutate_if(is.numeric,as.character)
DEG_up_exo_filtered_joined_sorted<-left_join(DEG_up_exo_filtered_joined, DEG_up_exo_int_counts, merge, by=c('V3' = 'Var1'))
DEG_up_exo_filtered_joined_sorted<- DEG_up_exo_filtered_joined_sorted %>% arrange(desc(ratio))
write.csv(DEG_up_exo_filtered_joined_sorted, file='DEG_up_candidates_sorted.csv')



#All interactions of exocyst
exocyst_int <- read.csv(file='../../exo_core/exocyst_int.csv', header=FALSE, sep=',', na.strings='NA')

#Filter out interactions with exo_core list
exo_core_7_10 <- read.csv(file='../../exo_core/exo_core_07_10.csv', header=TRUE, sep=',', na.strings='NA')
exocyst_int_filtered <- filter(exocyst_int, (exocyst_int$V10 %in% exo_core_7_10$code) != TRUE)
exocyst_int_filtered <- filter(exocyst_int_filtered, duplicated(exocyst_int_filtered[,c('V3', 'V10')]) != TRUE)
exocyst_int_filtered <- exocyst_int_filtered %>% mutate_if(is.factor,as.character)

#Are they in a GFP coll?
gfp_col <- read.csv(file='../../exo_core/gfp_col.csv', header=TRUE, sep=',', na.strings='NA')
in_gfp_col <- filter(gfp_col, (gfp_col$code %in% exocyst_int_filtered$V10) == TRUE)
in_gfp_col <- in_gfp_col %>% mutate_if(is.factor,as.character)
in_gfp_col$Observations <- NULL
str(in_gfp_col)

#append the info bout gfp coll to the list
exocyst_int_filtered_gfp <- left_join(exocyst_int_filtered, in_gfp_col, merge, by=c('V10' = 'code'))
write.csv(exocyst_int_filtered_gfp, file='../../exo_core/exocyst_int_gfp.csv')
exocyst_int_filtered_gfp_no <- as.data.frame(table(DEG_down_exo_int$V10))

#Cgeck frequency with what it is appearing in the list
exocyst_int_filtered_gfp_no <- as.data.frame(table(exocyst_int_filtered_gfp$V10))
exocyst_int_filtered_gfp_no <- exocyst_int_filtered_gfp_no %>% mutate_if(is.factor,as.character)
exocyst_int_filtered_gfp_rank <- left_join(exocyst_int_filtered_gfp, exocyst_int_filtered_gfp_no, merge, by=c('V10' = 'Var1'))
exocyst_int_filtered_gfp_rank <- exocyst_int_filtered_gfp_rank %>% group_by(V10)
exocyst_int_filtered_gfp_rank <- exocyst_int_filtered_gfp_rank %>% arrange(V10)
exocyst_int_filtered_gfp_rank <- exocyst_int_filtered_gfp_rank %>% arrange(desc(Freq))
str(exocyst_int_filtered_gfp_rank)
write.csv(exocyst_int_filtered_gfp_rank, file='../../exo_core/exocyst_int_gfp_rank.csv')





#check which genes from the upregulated at 12 degrees in sc have exocyst core machinery member as an interactor and write the result
result_down12_exo <- filter(int_down12_exo, (int_down12_exo$V11 %in% result_down12_sc$V3) == TRUE)
write.csv(result_down12_sc, file='exo_relevant_down_12_sc.csv')

#select cols with the expression data
down12sc <- down_at12_sc %>% select('gene', 'log2FoldChange')

#join them with the result file
result_down12_sc<-left_join(result_down12_sc, down12sc, merge, by=c('V3' = 'gene'))

#List of genes that are exocytosis related and downregulated at 12 degrees without duplicates
down_exo_list <- as.data.frame(result_down12_sc$V3)
down_exo_list <- distinct(down_exo_list)

#Search in the interactors of the genes from the list for the genes from the list (intersection, clustering)
result_up_inter_physical <- filter(up_within_physical, (up_within_physical$V10 %in% up_12_exo$V3) == TRUE)


