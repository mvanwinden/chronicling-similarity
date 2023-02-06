import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

parsedChronicles = 'GitHub\parsed_rotterdam_chronicles.ndjson'

def shingle(text: str, k: int):

    shingles = []

    for i in range(len(text) - k + 1):
        
        shingles.append(text[i:i+k])

    return set(shingles)

df = pd.read_json(parsedChronicles, lines = True)

df['date'] = df['date'].str.get(0).replace('-.*', '', regex= True)

df['date'] = df['date'].astype(str)

df['call_nr'] = df['call_nr'].str.replace('_.*', '', regex= True)

dfDateContents = df.pivot_table(values = 'text', index = 'date', columns = 'call_nr', aggfunc = 'sum', fill_value = np.nan)
dfDateContentsBack = df.pivot_table(values = 'text', index = 'date', columns = 'call_nr', aggfunc = 'sum', fill_value = 0)

dfDateContentsBack[dfDateContentsBack != 0] = 1
dfDateContentsBack = dfDateContentsBack.astype(int)
dfDateContentsBack = dfDateContentsBack[(dfDateContentsBack.T != 0).any()]


df1 = dfDateContentsBack.iloc[:len(dfDateContentsBack.index)//3, :]
df2 = dfDateContentsBack.iloc[len(dfDateContentsBack.index)//3: 2*(len(dfDateContentsBack.index)//3), :]
df3 = dfDateContentsBack.iloc[2*(len(dfDateContentsBack.index)//3):, :]

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10, 20), gridspec_kw={'width_ratios': [1,1,1], 'wspace': 0.3})
sns.heatmap(df1, cmap = 'Reds', vmin = 0.5, vmax = 1.5, ax=axs[0], linewidths=0.5, linecolor='black', cbar=False)
axs[0].set_title('')
axs[0].set_xlabel('')
axs[0].set_ylabel('Years')

sns.heatmap(df2, cmap = 'Reds', vmin = 0.5, vmax = 1.5, ax=axs[1], linewidths=0.5, linecolor='black', cbar=False)
axs[1].set_title('Years present in chronicle')
axs[1].set_xlabel('Chronicles')
axs[1].set_ylabel(' ')

sns.heatmap(df3, cmap = 'Reds', vmin = 0.5, vmax = 1.5, ax=axs[2], linewidths=0.5, linecolor='black', cbar=False)
axs[2].set_title('')
axs[2].set_xlabel('')
axs[2].set_ylabel(' ')

plt.show()

for column in dfDateContents.columns:

    if dfDateContents[column].dtype == "object":

        dfDateContents[column] = dfDateContents[column].str.replace('[^\w]','', regex = True)

        dfDateContents[column] = dfDateContents[column].str.lower()
        
        dfDateContents[column] = dfDateContents[column].apply(lambda x: shingle(str(x), 3) if pd.notna(x) else x)
    
columnPairs = list(itertools.combinations(dfDateContents.columns, 2))

dfJaccardSimilarities = pd.DataFrame(index = dfDateContents.index, columns = columnPairs)

dfJaccardSimilarities.rename(columns = {col: ", ".join(col) for col in dfJaccardSimilarities.columns}, inplace = True)

jSimList = []

for n in range(len(columnPairs)):

    for date in dfDateContents.index:

        if pd.notna(dfDateContents.at[date, columnPairs[n][0]]) and pd.notna(dfDateContents.at[date, columnPairs[n][1]]):

            jSim = []

            fileOne = dfDateContents.at[date, columnPairs[n][0]]

            fileTwo = dfDateContents.at[date, columnPairs[n][1]]

            jaccardSimilarity = len(fileOne.intersection(fileTwo)) / len(fileOne.union(fileTwo))

            jSim = [columnPairs[n], date, jaccardSimilarity]

            jSimList.append(jSim)

for x, y, value in jSimList:

    x = ', '.join(x)
    
    dfJaccardSimilarities.loc[y, x] = value

dfJaccardSimilarities.dropna(how = 'all', inplace = True)

dfJaccardSimilarities = dfJaccardSimilarities.apply(pd.to_numeric, errors = 'coerce')

sns.set(rc={'figure.figsize': (10, 30)})

sns.heatmap(dfJaccardSimilarities, cmap = sns.cm.rocket_r, vmin = 0, vmax = 1, linewidths=0.0, linecolor='black', annot = False)

plt.title('Jaccard Similarities Heat Map')
plt.xlabel('Chronicle pairs')
plt.ylabel('Year')

plt.show()
