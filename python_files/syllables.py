import pandas as pd
import numpy as np
import syllapy as syl

pd.options.mode.chained_assignment = None

file_path = './'
f = 'msgs_for_plos_one.csv'

df = pd.read_csv(file_path + f, sep= ',')
ai_df = df[df['Treatment'].isin(['AI'])]
control_df = df[df['Treatment'].isin(['Control'])]


# ai_df['split_msg'] = ai_df['Message'].apply(lambda msg: msg.split(' '))

dfs = [ai_df, control_df]

for d in dfs:
    d['split_msg'] = d['Message'].apply(lambda msg: msg.split(' '))
    d['syll_count'] = d['split_msg'].apply(lambda arr: [syl.count(msg) for msg in arr])
    d['avg_syll'] = d['syll_count'].apply(lambda arr: np.mean(arr))
    d['median_syll'] = d['syll_count'].apply(lambda arr: np.median(arr))

print(f"avg syllable count per message (AI) {np.mean(ai_df['avg_syll'])}")
print(f"avg syllable count per message (Control) {np.mean(control_df['avg_syll'])}")
print('\n\n')
print(f"median syllable count per message (AI) {np.median(ai_df['avg_syll'])}")
print(f"median syllable count per message (Control) {np.median(control_df['avg_syll'])}")

