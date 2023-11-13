#############################################################################
#install necessary packages
# install.packages('dplyr')
# install.packages('stringr')
# install.packages('udpipe')
# install.packages('flextable')
# install.packages('here')
##for easy cp -- remotes to access github
# install.packages('remotes')
# remotes::install_github('rlesur/klippy')


#############################################################################
#load packages
pacman::p_load(dplyr, stringr, udpipe, lattice, tm)

#############################################################################

#load 4 language models from udpipe
##english-ewt
ewt <- udpipe_download_model(language = 'english-ewt')
ewtPath <- ewt$file_model
ewtLoaded <- udpipe_load_model(file = ewtPath)
##english-gum
gum <- udpipe_download_model(language = 'english-gum')
##english-lines
enLines <- udpipe_download_model(language = 'english-lines')
##english-partut
part <- udpipe_download_model(language = 'english-partut')


#############################################################################

#load the csv file to introduce the model
fp <- './'
f <- 'msgs_for_plos_one.csv'

dataF <- read.csv(paste(fp,f,sep = ''))

aiDF <- dataF %>% dplyr::filter(,grepl('AI',Treatment))
controlDF <- dataF %>% dplyr::filter(,!grepl('AI',Treatment))

aiMainStr <- paste(aiDF$Message,collapse = ' ')
controlMainStr <- paste(controlDF$Message, collapse = ' ')

#############################################################################

#cleaning the amalgamated strings
#squish
aiMainStr <- aiMainStr %>% str_squish()
controlMainStr <- controlMainStr %>% str_squish()


#############################################################################

#annotating the strings;
aiAnnotated <- udpipe_annotate(ewtLoaded, x = aiMainStr)  %>% as.data.frame() %>% 
	select(-sentence)
controlAnnotated <- udpipe_annotate(ewtLoaded, x=controlMainStr) %>% 
	as.data.frame()  %>% 
	select(-sentence)

#checking frequency 
aiPosFreq <- txt_freq(aiAnnotated$upos)
contPosFreq <- txt_freq(controlAnnotated$upos)


#############################################################################

#checking syllable lengths
library(nsyllable)

aiDF$syllableCount <- lapply(aiDF$Message,FUN =  function(msg) {
	nsyllable(msg,use.names = FALSE)
})
controlDF$syllableCount <- lapply(controlDF$Message, FUN = function(msg){
	nsyllable(msg, use.names = FALSE)
})

mean(as.numeric(aiDF$syllableCount))
mean(as.numeric(controlDF$syllableCount))
