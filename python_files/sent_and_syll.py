import pandas as pd
import numpy as np
import csv
##############################################################################
#sentiment analysis
##############################################################################
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
##############################################################################
#syllable analysis
##############################################################################
import syllapy as syl

pd.options.mode.chained_assignment = None

file_path = './'
f = 'msgs_for_plos_one.csv'

df = pd.read_csv(file_path+f,sep=',')
ai_df = df[df['Treatment'].isin(['AI'])]
cont_df = df[df['Treatment'].isin(['Control'])]


##############################################################################
#checking sentiment with positive & negative words
##############################################################################

lemma = WordNetLemmatizer()
sent = SentimentIntensityAnalyzer()
stp_wds = stopwords.words('english')

def prep_txt(msg):
    corp = str(msg).lower()
    corp = re.sub('[^a-zA-Z]+',' ', corp).strip() #regex stripping
    tokens = word_tokenize(corp)
    words = [t for t in tokens if t not in stp_wds]
    lemmatize = [lemma.lemmatize(w) for w in words]
    return lemmatize

##positive & negative word file can be accessed with the following terminal cmds
###curl -O https://ptrckprry.com/course/ssd/data/positive-words.txt
###curl -O https://ptrckprry.com/course/ssd/data/negative-words.txt

dfs = [ai_df, cont_df]
file = open('./negative-words.txt','r', encoding='ISO-8859-1')
neg_wds = file.read().split()
file = open('./positive-words.txt','r', encoding='ISO-8859-1')
pos_wds = file.read().split()



for d in dfs:
    preprocess_tag = [prep_txt(i) for i in d['Message']]
    d['preprocess_txt'] = preprocess_tag
    d['total_length'] = d['preprocess_txt'].map(lambda x: len(x))
    num_positive = d['preprocess_txt'].map(lambda x: len([i for i in x if i in pos_wds]))
    num_negative = d['preprocess_txt'].map(lambda x: len([i for i in x if i in neg_wds]))
    d['pos_count'] = num_positive
    d['neg_count'] = num_negative
    d['sentiment'] = round((d['pos_count'] - d['neg_count'])/d['total_length'],4)
    #removing total_length calculation and adding 1 to denominator
    d['semi_normalized_sentiment'] = round(d['pos_count']/(d['neg_count'] + 1),4) 
    ##vader sentiment
    polarity = [round(sent.polarity_scores(i)['compound'],2) for i in d['Message']]
    d['vader_polarity_sentiment_score_(rng:-1/1)'] = polarity
    d['split_msg'] = d['Message'].apply(lambda msg: msg.split(' '))
    d['syll_count_by_word'] = d['split_msg'].apply(lambda arr: [syl.count(msg) for msg in arr])
    d['avg_syll'] = d['syll_count_by_word'].apply(lambda arr: np.mean(arr))
    d['median_syll'] = d['syll_count_by_word'].apply(lambda arr: np.median(arr))

final_df = pd.concat(dfs, ignore_index=True, sort=False)
final_df.to_csv('msg_for_plos_one_ammended.csv')

