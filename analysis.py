from wordcloud import WordCloud, STOPWORDS
from empath import Empath
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import database

# Feel free to modify
CATEGORIES_IN_HISTOGRAM = 20

#------------------------------------------------------------------------------------------
#- Dataframes -----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
works_1 = database.get_works("dataset1")
dataframe_1 = pd.DataFrame(data=works_1, columns=["title", "authors", "abstract"])

works_2 = database.get_works("dataset2")
dataframe_2 = pd.DataFrame(data=works_2, columns=["title", "authors", "abstract"])

works_3 = database.get_works("dataset3")
dataframe_3 = pd.DataFrame(data=works_3, columns=["title", "authors", "abstract"])

dataframes = [dataframe_1, dataframe_2, dataframe_3]

#------------------------------------------------------------------------------------------
#- WordCloud ------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
wordclouds = []

for data_index in range(len(dataframes)):
    dataframe = dataframes[data_index]
    comment_words = ""
    for index, data in dataframe.iterrows():
        text = (str(data["title"]) + " " + str(data["abstract"])).lower()
        
        tokens = text.split(); i = 0
        while i < len(tokens):
            # Remove non-letter symbols from token
            tokens[i] = "".join(filter(str.isalpha, tokens[i]))
            # Remove single-letter tokens
            if len(tokens[i]) < 2:
                tokens.pop(i)
                continue
            i += 1
        
        tokens = " ".join(tokens)
        comment_words += tokens + " "

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = set(STOPWORDS),
                    min_font_size = 10).generate(comment_words)
    
    wordclouds.append(wordcloud)

#------------------------------------------------------------------------------------------
#- Empath ---------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
lexicon = Empath()
normalized_categories: dict[dict] = {}

for data_index in range(len(dataframes)):
    dataframe = dataframes[data_index]
    
    total_sum = 0
    category_sums = {}
    for index, data in dataframe.iterrows():
        text = (str(data["title"]) + " " + str(data["abstract"])).lower()
        
        categories = lexicon.analyze(text, normalize=True)
        for cat, val in categories.items():
            # Initialize or add to the global sum for each category
            total_sum += val
            if cat in category_sums.keys():
                category_sums[cat] += val
            else:
                category_sums[cat] = val

    # Sort categories to extract N best matching categories (becomes a list temporarily)
    category_sums = sorted(category_sums.items(), key=lambda item: item[1], reverse=True)[:CATEGORIES_IN_HISTOGRAM]
    # Normalize data by dividing values by total sum (turn back into dictionary)
    category_sums = dict([(key, value/total_sum) for key, value in category_sums])

    # Save normalized categories to global dictionary for further analysis
    normalized_categories["dataset" + str(data_index + 1)] = category_sums

#------------------------------------------------------------------------------------------
#- Correlations ---------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
data1: dict = normalized_categories["dataset1"]
data2: dict = normalized_categories["dataset2"]
data3: dict = normalized_categories["dataset3"]
categories = data1.keys()

# Calculate correlation coefficient for each pair
# Result is a matrix like:
#  [1, coefficient]
#  [coefficient, 1]
# So we extract correct number with [0, 1]

corr1_2 = np.corrcoef(
    [data1.get(key, 0) for key in categories],
    [data2.get(key, 0) for key in categories]
)[0, 1]

corr1_3 = np.corrcoef(
    [data1.get(key, 0) for key in categories],
    [data3.get(key, 0) for key in categories]
)[0, 1]

corr2_3 = np.corrcoef(
    [data2.get(key, 0) for key in categories],
    [data3.get(key, 0) for key in categories]
)[0, 1]

#------------------------------------------------------------------------------------------
#- Visuals --------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# Create figure for wordclouds and category histograms
plt.rcParams["toolbar"] = "None"
fig, ((a11, a12), (a21, a22), (a31, a32)) = plt.subplots(nrows=3, ncols=2, width_ratios=[3,1], figsize=(18, 10))
fig.suptitle("Dataset categories and wordclouds (Q to exit)")

# Set dataset labels
a11.set_ylabel("Dataset 1")
a21.set_ylabel("Dataset 2")
a31.set_ylabel("Dataset 3")

# Configure and display wordclouds
a12.axis("off")
a22.axis("off")
a32.axis("off")
a12.imshow(wordclouds[0])
a22.imshow(wordclouds[1])
a32.imshow(wordclouds[2])

plt.tight_layout()
plt.get_current_fig_manager().full_screen_toggle()

# Display category-histograms
# Data variables point to previously calculated normalized category distributions
plt.setp(a11.get_xticklabels(), rotation=-10, ha="left", rotation_mode="anchor")
plt.setp(a21.get_xticklabels(), rotation=-10, ha="left", rotation_mode="anchor")
plt.setp(a31.get_xticklabels(), rotation=-10, ha="left", rotation_mode="anchor")
a11.set_xlim(-0.5, 19.5)
a11.bar(data1.keys(), data1.values(), width=1)
a21.set_xlim(-0.5, 19.5)
a21.bar(data2.keys(), data2.values(), width=1)
a31.set_xlim(-0.5, 19.5)
a31.bar(data3.keys(), data3.values(), width=1)

# Create smaller figure for correlation values
fig, (a1, a2, a3, a4) = plt.subplots(nrows=4, ncols=1, figsize=(5, 1.5))

a1.axis("off")
a2.axis("off")
a3.axis("off")
a4.axis("off")

a1.text(-0.15, 0, "Correlation between datasets:", fontsize=23)
a2.text(-0.1, 0, "1-2: " + str(round(corr1_2, 2)), fontsize=20)
a3.text(-0.1, 0, "1-3: " + str(round(corr1_3, 2)), fontsize=20)
a4.text(-0.1, 0, "2-3: " + str(round(corr2_3, 2)), fontsize=20)

plt.show()