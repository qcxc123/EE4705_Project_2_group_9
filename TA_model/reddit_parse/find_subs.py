# This Python file was written by Rachel

"""
Filter academically relevant subreddits from list of all subreddits and return filtered list and number of comments
"""

import json
import pandas as pd
import os

## get list of subreddits from saved txt file
with open("sub_list.txt", "r") as f:
    contents = f.readlines()
        
subreddit_lst = [k[:-1] for k in contents]
subreddit_lst = list(dict.fromkeys(subreddit_lst)) # unique
subreddit_lst.sort()
total = len(subreddit_lst)

## get number of samples for each subreddit from saved csv
freq = {}
for file in os.listdir('logs/'):
    filename = os.fsdecode(file)
    path = os.path.join('logs/', filename)
    df = pd.read_csv(path)    
    for index, row in df.iterrows():
        if row['sub_name'] in freq:
            freq[row['sub_name']] += row['count']
        else:
            freq[row['sub_name']] = row['count']     

## hardcoded keywords for academic subreddits
keywords_dict = {
    'science': ['science','physics','biology','chemistry','mathematics','theory','philosophy','engin','engineering','astronomy','earth',\
                'mathematics','medical','chemical','geology','medicine','knowledge','maths','bigbang','microscope','solarsystem','atom'\
                'environment','zoology','bacteria','electricity','electrical','programming','coding','programme','anthropology','ecology'\
                ],
    'economics': ['economics','economy','stocks','accounting','business','investment','banking','finance','income','marketanalysis',\
                  'inflation','fiscal','monetary','money'],
    'government': ['politics','government','election','capitalis','democracy','law','civilservice','bureaucracy','parliament','ministry'],
    'history': ['history','artifact','ancient','civilization','proletariat','bourgeoise'],
    'psychology': ['psychology','psychiatry','counselling','sociology'],
    }

keywords_lst = []
for lst in keywords_dict.values():
    for word in lst:
        if word not in keywords_lst:
            keywords_lst.append(word)
print("%d keywords" % len(keywords_lst))

## filter subreddits with keywords in name
num_samples = 0
filtered = []
for sub in subreddit_lst:
    contains = [k for k in keywords_lst if k in sub.lower()]
    if len(contains):
        filtered.append(sub)
        if sub in freq:
            num_samples += freq[sub]

## append filtered list of subreddits to txt file for transfer to json
with open('filtered_sub_list.txt', 'w') as g:
    for i in filtered:
        g.write('"%s",\r' % i)
filtered_len = len(filtered)
print("%d/%d subreddits(%.1f%%)" % (filtered_len, total, filtered_len/total*100))
print("%d/%d comments" % (num_samples, sum([k for k in freq.values()])))
