import nltk
import pandas as pd
import numpy as np
from nltk import tag, word_tokenize
from nltk.corpus import stopwords

pd.options.mode.chained_assignment = None

class PosTagger:
    def __init__(self, adjectives=None, adverbs=None, nouns=None, conjunctions=None, verbs=None, pronouns=None, prepositions=None):
        self.adjectives = adjectives or []
        self.adverbs = adverbs or []
        self.nouns = nouns or []
        self.conjunctions = conjunctions or []
        self.verbs = verbs or []
        self.pronouns = pronouns or []
        self.prepositions = prepositions or []

    def display_words(self, category):
        if category == 'adjectives':
            print("Adjectives:", ', '.join(self.adjectives))
        elif category == 'adverbs':
            print("Adverbs:", ', '.join(self.adverbs))
        elif category == 'nouns':
            print("Nouns:", ', '.join(self.nouns))
        elif category == 'conjunctions':
            print("Conjunctions:", ', '.join(self.conjunctions))
        elif category == 'verbs':
            print("Verbs:", ', '.join(self.verbs))
        elif category == 'pronouns':
            print("Pronouns:", ', '.join(self.pronouns))
        elif category == 'prepositions':
            print("Prepositions:", ', '.join(self.prepositions))
        else:
            print("Invalid category")

    def parse_and_increment(self, tup):
        cat = tup[1]
        val = tup[0]
        if cat not in ['IN','JJ','JJR','JJS','NN','NNP','NNS','PRP','PRP$','RB',
            'RBR', 'RBS','VB','VBD','VBG','VBN','VBP','VBZ','WP','WRB']:
            return
        if cat in ['IN','TO']:
            self.prepositions.append(val)
        elif cat in ['JJ','JJR','JJS']:
            self.adjectives.append(val)
        elif cat in ['NN','NNP', 'NNS']:
            self.nouns.append(val)
        elif cat in ['PRP','PRP$','WP']:
            self.pronouns.append(val)
        elif cat in ['RB','RBR', 'RBS','WRB']:
            self.adverbs.append(val)
        elif cat in ['VB','VBD','VBG','VBN','VBP','VBZ']:
            self.verbs.append(val)





file = './msgs_for_plos_one_ammended.csv'
df = pd.read_csv(file)
ai_df = df[df['Treatment'].isin(['AI'])]
control_df = df[df['Treatment'].isin(['Control'])]

dfs = [ai_df, control_df]

for d in dfs:
    d['tokenized'] = d['Message'].apply(lambda msg: word_tokenize(msg))
    tagged = d['tokenized'].apply(lambda msg: [nltk.pos_tag([token]) for token in msg])
    array_to_append = []
    for t in tagged:
        obj = PosTagger()
        for o in t:
            obj.parse_and_increment(o[0])
        array_to_append.append({
            'prepositions':len(obj.prepositions),
            'adjectives':len(obj.pronouns),
            'adverbs':len(obj.adverbs),
            'pronouns':len(obj.pronouns),
            'nouns':len(obj.nouns),
            'verbs':len(obj.verbs),
            'prepositions':len(obj.prepositions)
        })
    d['pos_tagging'] = array_to_append

final_df = pd.concat([ai_df,control_df], ignore_index=True, sort=False)
final_df.to_csv('msgs_for_plos_one_ammended_v2.csv')
