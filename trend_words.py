import os, sys, operator, math
from collections import Counter

directory = './tweets-model/'
directory_bigram = './tweets-model-bigram/'

"""
Create trend of the day by comparing the model of the day with the previous days models:
1) The frequency should > 1e-5
2) The frequency should at least doubled than previous models
"""
def process_trend(directory):
    days = []

    for file in sorted(os.listdir(directory)):
        if file.endswith('.csv'):
            days.insert(0, file)
    # Process current day only
    # for i in range(len(days)-1):
    prevModel = {}
    currModel = {}
    hotWords = {}

    # Use 14 day's summary model as prev
    prevIndex = len(days)-1 if len(days) <= 15 else 15
    prevWords = {}
    total_words_len = 0
    for day in days[1:prevIndex]:
        with open(directory+day, 'r') as f:
            daily_words_len = int(day.split('-')[-1].split('.')[0])
            total_words_len += daily_words_len
            for token in f.readlines():
                if token:
                    word, prob = token.split(',')[0], float(token.split(',')[1])
                    if word in prevWords:
                        prevWords[word] += prob * daily_words_len
                    else:
                        prevWords[word] = prob * daily_words_len
    for word in prevWords:
        prevModel[word] = prevWords[word] / total_words_len
    

    with open(directory+days[0], 'r') as f:
        for token in [t for t in f.readlines() if t]:
            if token:
                word, prob = token.split(',')[0], float(token.split(',')[1])
                if prob > 1e-5:
                    currModel[word] = prob

    for word in currModel.keys():
        if word in prevModel:
            rate = currModel[word] / prevModel[word]
            if rate > 2.0:
                hotWords[word] = (currModel[word], math.log2(rate))
        else:
            hotWords[word] = (currModel[word], 0)


    outdir = './tweets-trend/' if directory == './tweets-model/' else './tweets-trend-bigram/'
    with open(outdir+'trend-'+days[0].split('-')[1]+'.csv', 'w') as f:
        f.write('word, today\'s frequency, log2(freq.today/freq.ystdy)\n')
        [f.write('{0},{1},{2}\n'.format(key, value[0], value[1])) for key, value in hotWords.items()]

    print(days[0], len(hotWords))

process_trend(directory)
process_trend(directory_bigram)
