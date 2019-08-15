import string
import pandas as pd
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import os
import HTMLParser
import json


#   matches each tweet to brand(s)
def match_tweets(tweets, brand_list):
    brand_tweets = {i: [] for i in brand_list}
    for tweet in tweets:
        tweet_text = tweet['clean_text']
        name = cleanup_text(tweet['name'])
        screen_name = cleanup_text(tweet['screen_name'])
        hashtags = " ".join(tweet['hashtags'])
        search_string = tweet_text + " " + name + " " + screen_name + " " + hashtags
        search_string = search_string.lower()
        for brand in brand_list:
            if brand in search_string:
                brand_tweets[brand].append(tweet)
    return brand_tweets


#   checks whether the sentiment of the tweet is positive, neutral, or negative
def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


#   tries to remove emojis from a string
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


#   removes unecessary words/punctuation/chars to create a clean string
def cleanup_text(text):
    #   escaping HTML characters
    html_parser = HTMLParser.HTMLParser()
    text = html_parser.unescape(text)
    #   remove emojis from string
    text = deEmojify(text)
    #   declare stop words and removes stop words below
    stop_words = set(stopwords.words('english'))
    #   remove urls from tweet
    text = re.sub(r"http\S+", "", text)
    word_tokens = word_tokenize(text)

    filtered_text = []

    for w in word_tokens:
        if w not in stop_words and w not in string.punctuation:
            filtered_text.append(w)
    return ' '.join(filtered_text).lower()


#   adds clean text and sentiment to the data set to be loaded as csv
def pre_process_tweets(tweets):
    data = []
    for tweet in tweets:
        tweet['clean_text'] = cleanup_text(tweet['text'])
        tweet['sentiment'] = get_sentiment(tweet['clean_text'])
        data.append(tweet)
    return data


#   deletes old csv before processing new csv
def deleteCSV():
    filelist = [f for f in os.listdir('../data/processed/') if f.endswith('.csv')]
    for f in filelist:
        os.remove(os.path.join('../data/processed/', f))


#   writes the data for each brand to a csv file
def write_to_csv_version(data, file, brand):
    global csvFile
    csv_columns = ['screen_name', 'sentiment', 'text', 'created_at', 'hashtags', 'source', 'location', 'clean_text',
                   'retweet_count', 'favorite_count', 'name']

    df = pd.DataFrame(columns=csv_columns)

    for tweet in data:
        tweet_df = pd.DataFrame([tweet], columns=csv_columns)
        df = df.append(tweet_df, ignore_index=True)
        csvFile = open(file, 'a')
    df.to_csv(csvFile, mode='a', columns=csv_columns, index=False, encoding='utf-8')


def main():
    try:
        with open('../data/raw/raw_tweet_data.json') as file:
            data = json.load(file)
            brand_names_list = ['tesla', 'honda', 'jaguar', 'mercedes', 'ford']
            data = pre_process_tweets(data)
            matching_brands = match_tweets(data, brand_names_list)
            brands_prefix = '../data/processed/'
            deleteCSV()
            for brand in brand_names_list:
                brand_path = brands_prefix + brand + '.csv'
                if len(matching_brands[brand]) > 0:
                    write_to_csv_version(matching_brands[brand], brand_path, brand)
    except IOError:
        print ('An error occurred, check if the raw json file exists!')


if __name__ == '__main__':
    main()
