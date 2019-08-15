import os

import matplotlib as mpl
import pandas as pd

mpl.use('TkAgg')

import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np


#   gets the value of the sentiment or sets to 0 if there is no key
def get_value_sentiment(sentiments, type):
    value = 0
    if type in sentiments:
        value = sentiments[type]
    return value


#   gets the sum of rewteets for the specific brand using all tweets
def get_retweets(path, root):
    full_path = root + path
    df = pd.read_csv(full_path)
    retweets = df['retweet_count'].sum()
    return retweets


#   gets the sum of favorites for the specific brand using all tweets
def get_favorites(path, root):
    full_path = root + path
    df = pd.read_csv(full_path)
    favorites = df['favorite_count'].sum()
    return favorites


#   creates a bar graph per brand that graphs the sentiments of the collection of tweets
def sentiment_analysis(path, root):
    full_path = root + path
    df = pd.read_csv(full_path)
    sentiments = df.groupby('sentiment').size()
    positive = get_value_sentiment(sentiments, 'positive')
    neutral = get_value_sentiment(sentiments, 'neutral')
    negative = get_value_sentiment(sentiments, 'negative')

    objects = ('Positive', 'Neutral', 'Negative')
    y_pos = np.arange(len(objects))
    sentiment_values = [positive, neutral, negative]

    plt.bar(y_pos, sentiment_values, align='center', alpha=1.0, color=(0.2, 0.4, 0.6, 0.6))
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Tweets')
    company = os.path.splitext(path)[0]
    plt.title('Sentiment for ' + company.upper())
    plt.savefig('../analysis/sentiment_analysis/' + company + '_sentiment_analysis' + '.png')
    plt.close()


#   creates a word cloud per brand that shows the most frequent words used in the tweets
def word_analysis(path, root):
    full_path = root + path
    df = pd.read_csv(full_path)
    clean_text = df['clean_text'].tolist()

    all_words = ' '.join([text for text in clean_text])
    print(all_words)
    from wordcloud import WordCloud
    wordcloud = WordCloud(width=900, height=700, random_state=21, max_font_size=110, collocations=False).generate(
        all_words)
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    company = os.path.splitext(path)[0]
    plt.savefig('../analysis/word_analysis/' + company + '_wordcloud.png')
    plt.close()


#   creates a double bar graph that compares the favorite and retweet counts per brand
def retweets_favorites_analysis(retweets, favorites, brands):
    N = len(brands)
    ind = np.arange(N)
    width = 0.35
    plt.bar(ind, retweets, width, label='Retweets')
    plt.bar(ind + width, favorites, width,
            label='Favorites')

    plt.ylabel('Number of retweets/favorites')
    plt.title('Retweets/Favorites by Vehicle Company')

    plt.xticks(ind + width / 2, brands)
    plt.legend(loc='best')
    plt.savefig('../analysis/retweets_favorites_analysis/' + 'retweets_favorites_analysis.jpeg')
    plt.close()


def main():
    rootdir = '../data/processed/'

    paths = []
    retweets = []
    favorites = []
    brands = []

    print('Running Data Analysis...')
    for path in os.listdir(rootdir):
        if not path.startswith('.'):
            sentiment_analysis(path, rootdir)
            word_analysis(path, rootdir)

            company = os.path.splitext(path)[0]
            brands.append(company)

            retweets.append(get_retweets(path, rootdir))
            favorites.append(get_favorites(path, rootdir))
    retweets_favorites_analysis(retweets, favorites, brands)
    print('Data Analysis Complete!')

if __name__ == '__main__':
    main()
