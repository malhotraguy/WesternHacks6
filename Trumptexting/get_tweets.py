import csv
import re

import tweepy

from helper import get_credentials

consumer_creds = get_credentials("./secrets/consumer_credentials.json")
access_creds = get_credentials("./secrets/access_credentials.json")
consumer_key = consumer_creds["consumer_key"]
consumer_secret = consumer_creds["consumer_secret"]
access_key = access_creds["access_key"]
access_secret = access_creds["access_secret"]


def get_all_tweets(screen_name):
    all_tweets = []
    new_tweets = []

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    client = tweepy.API(auth)
    new_tweets = client.user_timeline(screen_name=screen_name, count=200)

    while len(new_tweets) > 0:
        for tweet in new_tweets:
            if tweet.source == "Twitter for iPhone":
                all_tweets.append(tweet.text)

        print("We've got %s tweets so far" % (len(all_tweets)))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(
            screen_name=screen_name, count=200, max_id=max_id
        )

    return all_tweets


def clean_tweet(tweet):
    tweet = re.sub("https?\:\/\/", "", tweet)  # links
    tweet = re.sub("#\S+", "", tweet)  # hashtags
    tweet = re.sub("\.?@", "", tweet)  # at mentions
    tweet = re.sub("RT.+", "", tweet)  # Retweets
    tweet = re.sub("Video\:", "", tweet)  # Videos
    tweet = re.sub("\n", "", tweet)  # new lines
    tweet = re.sub("^\.\s.", "", tweet)  # leading whitespace
    tweet = re.sub("\s+", " ", tweet)  # extra whitespace
    tweet = re.sub("&", "and", tweet)  # encoded ampersands
    return tweet


def write_tweets_to_csv(tweets):
    with open("tweets.csv", "w") as f:
        writer = csv.writer(f)
        for tweet in tweets:
            tweet = clean_tweet(tweet)
            if tweet:
                writer.writerow([tweet.encode("utf-8")])


if __name__ == "__main__":
    tweets = get_all_tweets("realdonaldtrump")
    write_tweets_to_csv(tweets)
