# What is this?

The Gartner Coding Challenge is a case study that explores the benchmarking of search visibility for different vehicle brands.
The data used to benchmark search visibility are tweets from twitter.

This project provides a solution to this case study. The case study itself is made up of four major steps: 

1. **Automatic Data Collection:** Data is read from twitter using a combined query on an hourly basis.
2. **Matching:** Each tweet is categorized/matched to a vehicle brand, such as "Tesla" or "Honda".
3. **Storing Data:** The raw data itself is stored in a JSON file. The matched data is stored in CSV files per brand. 
4. **Data Analysis:** There is basic data analysis performed to show the value of collecting tweets and using them to gauge brand 
   brand awareness. 


# Installation/Setup

The entire application is written using Python. These are the steps you must take to install and setup this application for use: 

1. Sign up for a twitter developer account. Create an application on the twitter account to obtain access to a consumer key, consumer secret key, access token, and secret access token.
2. Clone this repo onto your local.
3. Navigate to the src folder and open config.py. Update the config file with your credentials and save.
4. Now you are ready to load twitter data and perform analysis!


# How To Use

## Automatic Data Collection

The data collection itself happens on an hourly basis, 500 tweets at a time. The script that runs the data collection is named collect_twitter_data.py and it is located in the src folder.
In this script, the user can change a couple variables to customize the script as needed. The user can change the query variable in the main function to specify what they would like
to search for. Additionally, it is also possible to change the limit of tweets that are queried. This can be done in the search_tweets function in the "tweets" variable. 

To execute this script, run this command in terminal: 
    python collect_twitter_data.py &
    
This will run the script in the background until someone manually interrupts the process. In each interval, the script will look for relevant tweets that were made in the last hour, and dump 
them into a raw json file. This file is located in the "./data/raw" path and is named "raw_tweet_data.json". Newly queried tweets will all be dumped into this json file as long as the process
is running.

## Matching Tweets to Brand

The script that matches the tweets data in the json file to vehicle brands is named match_tweets_to_brand.py and is located in the src folder as well. 
The purpose of this script is to look for the json file and match each tweet from the json file to a vehicle brand. In this script, it is 
possible change the brand_names_list variable in the main function to add or remove vehicle brands with which the tweets will be matched.

To execute this script, run this command in terminal:
    python match_tweets_to_brand.py

This script does not run in the background. Once the script runs, new csv files are created in the "data/processed/" path by brand name based off the data that exists in the json file.
Each row in the csv file is information about a tweet that was matched with the brand, such as the text of the tweet, the hashtags used in the tweet, etc.


## Data Analysis

Once the csv files have been generated, data analysis can be performed. The analysis in this application focuses on how twitter data can be used to assess brand performance and awareness.
The script that is used to perform this analysis is named data_analysis_twitter.py and is also located in the src folder of the application.

To execute this script, run this command in terminal:
    python data_analysis_twitter.py

The analysis is performed in three parts: (1) - Sentiment Analysis, (2) - Word Analysis, (3) - Retweets/Favorites Analysis.

1. **Sentiment Analysis:** Within the aformentioned match_tweets_to_brand.py script, each tweet is assigned a sentiment as part of its pre-processing run.
These sentiment values are loaded into each csv file along with the data received from the Twitter API. The "sentiment" of a tweet is either "positive", "negative",
or "neutral". The data_analysis_twitter script counts these sentiment values and graphs them in a bar graph per vehicle brand. For example,
if Tesla has 40 positive tweets, 30 neutral tweets, and 10 negative tweets, this information is plotted in an individual bar graph. The sentiment bar graph for each vehicle is located
in "./analysis/sentiment_analysis".
    
2. **Word Analysis:** Another form of analysis is word frequency analysis, which is also done in the data_analysis_twitter.py script. The wordcloud
library is used to create a word cloud graph per brand. The more a word shows up in the tweets that are in the csv file for the brand, the larger the word is in the word cloud for the brand.
The word clouds per brand are located in "./analysis/word_analysis". 

3. **Retweets/Favorites Analysis:** The last form of analysis that is performed is counting the total number of retweets/favorites per brand and comparing them in a double bar graph. 
When thinking of brand awareness/performance using data from Twitter, the most prominent question that each brand should ask is "Is the world talking about our products?"
One of the ways with which we can try answering this question using real tweet data is by counting the number of favorites and retweets for each brand csv. A double bar graph is used for 
this analysis to display how the public is interacting with tweets and to compare each brands' results side by side with the other brands.

