import tweepy as tw
import time
import datetime
import json
import config
import os


#   return api client after user has been authenticated
def load_api_client():
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        raise e
    print('Client created...')
    return api


#   query for Tweets and write them to file
def search_tweets(query):
    api = load_api_client()
    tweets = tw.Cursor(api.search, q=query, lang="en", tweet_mode='extended').items(500)
    return tweets


#   write tweets to json file
def filtered_tweet(tweets):
    json_arr = []
    for tweet in tweets:
        json_content = {}
        #   starting point of checking for new tweets (tweets within the last hour)
        starting_point = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        if starting_point <= tweet.created_at:
            tweet_json = tweet._json
            json_content['created_at'] = tweet_json['created_at']
            json_content['source'] = tweet_json['source']
            json_content['text'] = tweet_json['full_text']
            json_content['favorite_count'] = tweet_json['favorite_count']
            json_content['retweet_count'] = tweet_json['retweet_count']
            json_content['screen_name'] = tweet_json['user']['screen_name']
            json_content['name'] = tweet_json['user']['name']
            json_content['hashtags'] = [hashtag_item['text'] for hashtag_item in tweet_json["entities"]["hashtags"]]
            json_content['location'] = tweet_json['user']['location']
            json_arr.append(json_content)
    return json_arr


#   write to json
def write_to_JSON_file(data):
    file_path_name = '../data/raw/raw_tweet_data.json'
    if not os.path.isfile(file_path_name):
        with open(file_path_name, mode='w') as f:
            f.write(json.dumps(data, indent=2))
    else:
        with open(file_path_name) as feedsjson:
            feeds = json.load(feedsjson)

        feeds = feeds + data
        with open(file_path_name, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))
    f.close()


#   search for tweets using query string
def main():
    query = 'ford OR jaguar OR automobile OR tesla OR honda OR automotive OR' \
            '"electric car" OR "ford focus" OR "jaguar" OR "motor trend"' + '-filter:retweets'
    print('Searching for Tweets...')
    tweets = search_tweets(query)
    filtered_tweets = filtered_tweet(tweets)
    print('Writing Tweets to JSON file...')
    write_to_JSON_file(filtered_tweets)


while True:
    print('Starting data collection process...')
    if __name__ == '__main__':
        main()
    print('Waiting before the next data collection process starts...')
    time.sleep(3600)
