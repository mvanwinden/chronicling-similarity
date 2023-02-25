import pandas as pd
import numpy as np
import seaborn as sns
import itertools
import matplotlib.pyplot as plt

def importCorpus(corpus):
    
    corpusDataFrame = pd.read_json(corpus, lines=True)
    corpusDataFrame['date'] = corpusDataFrame['date'].str[0].astype(str)
    contents = corpusDataFrame.pivot_table(values='text', index='date', columns='call_nr', aggfunc='sum', fill_value=np.nan)
    
    return contents

def prepareCorpus(contents):

    for column in contents.columns:

        if contents[column].dtype == 'object':

            contents[column] = contents[column].str.replace('[^\w]','', regex = True)
            contents[column] = contents[column].str.lower()
            contents[column] = contents[column].apply(lambda x: set([x[i:i+3] for i in range(len(x)-2)]) if pd.notna(x) else x)

    return contents

def jaccardSimilarity(contentsClean):

    chroniclePairs = list(itertools.combinations(contentsClean.columns, 2))

    jaccardSimilaritiesDataframe = pd.DataFrame(index = contentsClean.index, columns = chroniclePairs)

    jaccardSimilaritiesDataframe.rename(columns = {col: ", ".join(col) for col in jaccardSimilaritiesDataframe.columns}, inplace = True)

    jaccardSimilarityList = []

    for n in range(len(chroniclePairs)):

        for date in contentsClean.index:

            if pd.notna(contentsClean.at[date, chroniclePairs[n][0]]) and pd.notna(contentsClean.at[date, chroniclePairs[n][1]]):

                similarity = []

                fileOne = contentsClean.at[date, chroniclePairs[n][0]]
                fileTwo = contentsClean.at[date, chroniclePairs[n][1]]

                jaccardSimilarity = len(fileOne.intersection(fileTwo)) / len(fileOne.union(fileTwo))

                similarity = [chroniclePairs[n], date, jaccardSimilarity]

                jaccardSimilarityList.append(similarity)

    for x, y, value in jaccardSimilarityList:

        x = ', '.join(x)
        
        jaccardSimilaritiesDataframe.loc[y, x] = value

    jaccardSimilaritiesDataframe.dropna(how = 'all', inplace = True)
    jaccardSimilaritiesDataframe = jaccardSimilaritiesDataframe.apply(pd.to_numeric, errors = 'coerce')

    return jaccardSimilaritiesDataframe

def jaccardSimilarityHeatmap(jaccard_similarities):

    sns.set(rc={'figure.figsize': (10, 30)})
    sns.heatmap(jaccard_similarities, cmap=sns.cm.rocket_r, vmin=0, vmax=1, linewidths=0.0, linecolor='black', annot=False)
    plt.title('Jaccard Similarities Heat Map')
    plt.xlabel('Chronicle pairs')
    plt.ylabel('Year')
    return plt.gcf()

def main():

    corpus = 'parsed_rotterdam_chronicles.ndjson'
    contents = importCorpus(corpus)
    contentsClean = prepareCorpus(contents)
    jaccardSimilarities = jaccardSimilarity(contentsClean)
    heatmap = jaccardSimilarityHeatmap(jaccardSimilarities)
    plt.show(heatmap)
    
if __name__ == '__main__':

    main()
