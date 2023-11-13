## install necessary packages #############################################
#install.packages('tm')
#install.packages('SnowballC')
#install.packages('wordcloud')
#install.packages('RColorBrewer')

##########################################################################

# Load pkgs
library(tm)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)
library(dplyr)


##########################################################################

# load data into model, create one big string with AI and one without
filePath  <- './'
f <- 'msgs_for_plos_one.csv'

dataF <- read.csv(paste(filePath,f,sep = ''))

aiDF <- dataF %>% dplyr::filter(,grepl('AI', Treatment))

controlDF <- dataF %>% dplyr::filter(,!grepl('AI', Treatment))

#with values loaded into separate dataframes, combine text into one huge string

aiMainStr <- paste(aiDF$Message,collapse = ' ')
controlMainStr <- paste(controlDF$Message, collapse = ' ')


##########################################################################

#load data as corpus

aiCorp <- VCorpus(VectorSource(aiMainStr))
contCorp <- VCorpus(VectorSource(controlMainStr))


##########################################################################

#clean the text

##lowercase
aiCorp <- tm_map(aiCorp, content_transformer(tolower))
contCorp <- tm_map(contCorp, content_transformer(tolower))

##remvoe numbers
aiCorp <- tm_map(aiCorp, removeNumbers)
contCorp <- tm_map(contCorp, removeNumbers)

##remove common stopwords 
###this list of stopwords was sourced from 'https://gist.github.com/sebleier/554280'
#stopWordsFilePath <- './'
#stopWordsFile <- 'stopwords.txt'
#sWds <- scan(paste(stopWordsFilePath,stopWordsFile,sep=''),character(),quote="",
#						 sep='\n')

aiCorp <- tm_map(aiCorp, removeWords, stopwords('english'))
contCorp <- tm_map(contCorp, removeWords, stopwords('english'))

##remove punctuation
aiCorp <- tm_map(aiCorp, removePunctuation)
contCorp <- tm_map(contCorp, removePunctuation)


##########################################################################

# build the term document matrix {rows: documented instances, cols: words }
##docTermMtx
aiDTM <- DocumentTermMatrix(aiCorp)
contDTM <- DocumentTermMatrix(contCorp)
##convert to mtx
aiM <- as.matrix(aiDTM)
contM <- as.matrix(contDTM)
##frequeny values
aiV <- sort(colSums(aiM),decreasing = TRUE)
contV <- sort(colSums(contM),decreasing = TRUE)
##load into final dataframe 
aiFinalDF <- data.frame(word=names(aiV),freq=aiV)
controlFinalDF <- data.frame(word=names(contV),freq=contV)


##########################################################################

# let's build some clouds
## AI prompts
set.seed(1234)
wordcloud(words =controlFinalDF$word, freq = controlFinalDF$freq, min.freq = 1, 
					max.words = 140, random.order = FALSE, rot.per = 0.35, 
					colors = brewer.pal(8,"Dark2"))


##########################################################################

#looking at word associations with the doctermMatrix
aiAssoc <- findAssocs(aiDTM,terms = c("appreciation","thank","truly"),
											corlimit = .3)
contAssoc <- findAssocs(aiDTM,terms = c("appreciate","thank","team"),
												corlimit = .3)
