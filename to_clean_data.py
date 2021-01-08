# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 20:23:47 2020

@author: madyf
"""


import pandas as pd

#%%
#import all three review files

boston_reviews = pd.read_csv(r"C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\reviews.csv")
#nyc_reviews = pd.read_csv(r"C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\reviews_nyc.csv")
sea_reviews = pd.read_csv(r"C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\reviews_sea.csv")

#%% #https://www.kaggle.com/kimnganvu/sentiment-analysis-and-collocation-of-reviews 
# could not figure out how to fix this on my own and I tried several different ways
#this is to get only english reviews (so that vader can read them all)
from nltk.corpus import stopwords   # stopwords to detect language
from nltk import wordpunct_tokenize # function to split up our words

def get_language_likelihood(input_text):
    """Return a dictionary of languages and their likelihood of being the 
    natural language of the input text
    """
 
    input_text = input_text.lower()
    input_words = wordpunct_tokenize(input_text)
 
    language_likelihood = {}
    total_matches = 0
    for language in stopwords._fileids:
        language_likelihood[language] = len(set(input_words) &
                set(stopwords.words(language)))
 
    return language_likelihood
 
def get_language(input_text):
    """Return the most likely language of the given text
    """ 
    likelihoods = get_language_likelihood(input_text)
    return sorted(likelihoods, key=likelihoods.get, reverse=True)[0]
boston_reviews_clean = [r for r in boston_reviews['comments'] if pd.notnull(r) and get_language(r) == 'english']

sea_reviews_clean = [r for r in sea_reviews['comments'] if pd.notnull(r) and get_language(r) == 'english']
#%%
boston_clean_comments = boston_reviews_clean
#nyc_clean_comments = nyc_reviews_clean
sea_clean_comments = sea_reviews_clean

#%%
#need to delete all the rows of the og dataset that are not in the clean ones

comments_list = [boston_clean_comments, sea_clean_comments]
og_df_list = [boston_reviews, sea_reviews]

counter = 0
for df in og_df_list:
    current_og_df = og_df_list[counter]
    current_clean_comments = comments_list[counter]
    
    true_false_list = []
    for instance in range(0,len(current_og_df)):
        current_review = current_og_df.iloc[instance, 5]
        if current_review in current_clean_comments:
            true_false_list.append("True")
        else:
            true_false_list.append("False")
    current_og_df["true/false"] = true_false_list      
    counter += 1

#%%
#remove rows that are not true
clean_boston = boston_reviews[boston_reviews["true/false"] == "True"]
clean_sea = sea_reviews[sea_reviews["true/false"] == "True"]

#%%
#combine into one big df with a column for the city of the listing
df_list = [clean_boston, clean_sea]
thing_to_append_list = ["boston", "seattle"]

counter = 0
for df in df_list:
    current_df=df_list[counter]
    thing_to_append = thing_to_append_list[counter]
    
    temp = []
    for i in range(0,len(current_df)):
        temp.append(thing_to_append)
    df_list[counter]["city"]=temp
    counter += 1
#%%
reviews_df = pd.concat(df_list)

#%% next step is to obtain sentiment for each review
#there are several pre-created libraries to define sentiment, I have used VADER before and will use it for this project
#I will only use the compound score and not look at polarity or anything else
#ranges from -1 bad to 0 neutral to 1 good

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def sentiment_scorer(sentence):
    score = analyser.polarity_scores(sentence)
    return score['compound']
    


#%% calculate sentiment for every review

vader_score = []
for instance in range(0,len(reviews_df)):
    score_temp = sentiment_scorer(reviews_df.iloc[instance,5])
    vader_score.append(score_temp)
#%% add vader score column to the dataframe 

reviews_df["vader_score"] = vader_score
#%%
csv_data = reviews_df.to_csv(r'C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\clean_reviews_df.csv', index = False) 
#%% combine listings for boston and 

boston_listings = pd.read_csv(r"C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\listings.csv")
sea_listings = pd.read_csv(r"C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\listings_sea.csv")

#%%
to_concat = [boston_listings, sea_listings]
listings = pd.concat(to_concat)
#%% remove $ from price column

for i in range(0,len(listings)):
    temp = listings.iloc[i,60]
    temp_new = temp.replace("$","") 
    #print(temp_new)
    temp_new = temp_new.replace(".","")
    if "," in temp_new:
        temp_new = temp_new.replace(",","")
    #print(temp_new_2)
    temp_int = int(temp_new)
    temp_correct = temp_int/100

    listings.iloc[i,60] = temp_correct
    
#%%
csv_data = listings.to_csv(r'C:\Users\madyf\Documents\RUTGERS\Fall2020\Python\Project\both_listings.csv', index = False) 
