import pandas as pd
import numpy as np
import seaborn as sns
import itertools
import matplotlib.pyplot as plt

def importCorpus(corpus):
    
    corpusDataFrame = pd.read_json(corpus, lines=True)
    corpusDataFrame['date'] = corpusDataFrame['date'].str[0].astype(str)
    contents = corpusDataFrame.pivot_table(values = 'text', index = 'date', columns = 'call_nr', aggfunc = 'sum', fill_value=np.nan)
    
    return contents

def prepareCorpus(contents):

    for column in contents.columns:

        if contents[column].dtype == 'object':

            contents[column] = contents[column].str.replace('[^\w]','', regex = True)
            contents[column] = contents[column].str.lower()
            contents[column] = contents[column].apply(lambda x: set([x[i:i+3] for i in range(len(x)-2)]) if pd.notna(x) else x)

    return contents

def jaccardSimilarity(contentsClean):

    pairs = list(itertools.combinations(contentsClean.columns, 2))
    similarities = []
    
    for pair in pairs:
    
        for date in contentsClean.index:
    
            files = contentsClean.loc[date, list(pair)].dropna()
    
            if len(files) == 2:
    
                jaccard = len(files.iloc[0].intersection(files.iloc[1])) / len(files.iloc[0].union(files.iloc[1]))
    
                similarities.append([', '.join(pair), date, jaccard])
    
                jaccardSimilaritiesDataframe = pd.DataFrame(similarities, columns = ['Chronicle Pairs', 'Date', 'Jaccard Similarity'])
    
    jaccardSimilaritiesDataframe = jaccardSimilaritiesDataframe.pivot_table(values = 'Jaccard Similarity', index = 'Date', columns = 'Chronicle Pairs', aggfunc = 'sum', fill_value = np.nan)
    
    return jaccardSimilaritiesDataframe

def eventDistributionPlot(contents):

    contents = contents.fillna(0).applymap(lambda x: 1 if x!=0 else 0)

    sns.set(rc={'figure.figsize': (10, 30)})
    
    sns.heatmap(contents, cmap = 'Reds', vmin = 0.5, vmax = 1.5, linewidths = 0.5, linecolor = 'black', cbar = False)

    return plt.gcf()

def jaccardSimilarityHeatmap(jaccard_similarities):

    sns.set(rc={'figure.figsize': (10, 30)})
    sns.heatmap(jaccard_similarities, cmap=sns.cm.rocket_r, vmin = 0, vmax = 1)
    plt.title('Jaccard Similarities Heat Map')
    plt.xlabel('Chronicle pairs')
    plt.ylabel('Year')
    return plt.gcf()

def main():

    corpus = 'parsed_rotterdam_chronicles.ndjson'
    
    contents = importCorpus(corpus)
    contentsClean = prepareCorpus(contents)
    jaccardSimilarities = jaccardSimilarity(contentsClean)

    plt.figure()
    heatmap = jaccardSimilarityHeatmap(jaccardSimilarities)
    plt.savefig('jaccard_similarity_heatmap.svg', format = 'svg', dpi = 300, bbox_inches = 'tight')
    
    plt.figure()
    distribution = eventDistributionPlot(contents)
    plt.savefig('event_distribution_plot.svg', format='svg', dpi = 300, bbox_inches = 'tight')
    
if __name__ == '__main__':

    main()
