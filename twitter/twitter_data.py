"""Third party imports."""
import tweepy
import configparser
import pandas as pd
import time

# read configs

config = configparser.ConfigParser()
config.read("twitter/config.ini")

api_key = config["TWITTER"]["api_key"]
api_key_secret = config["TWITTER"]["api_key_secret"]

access_token = config["TWITTER"]["access_token"]
access_token_secret = config["TWITTER"]["access_token_secret"]


# authentication

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

twit_df = pd.read_csv('twitter\game_list.csv')
game_list= twit_df['game'].values.tolist()

def search_tweets(game):
    """Search tweets about a certain game."""
    columns = [
        "Time",
        "User",
        "Tweet",
        "Coordinates",
        "User Data",
        "Retweet Count",
        "Likes Count",
        "language",
    ]
    data = []
    limit = 10000
    retry_count = 3
    retry_delay = 5  # Number of seconds to wait between retries

    while retry_count > 0:
        try:
            tweets = tweepy.Cursor(
                api.search_tweets, q=f"%23{game}", count=100, tweet_mode="extended"
            ).items(limit)

            break  # If the code executes without an exception, break out of the loop
        except tweepy.TweepyException as e:
            print(f"An error occurred: {str(e)}")
            print("Retrying...")
            retry_count -= 1
            time.sleep(retry_delay)

    if retry_count == 0:
        print("Failed to send request after multiple retries. Check your network connection.")

    
    
    for tweet in tweets:
        likes_count = tweet.favorite_count
        if hasattr(tweet, 'retweeted_status'):
            likes_count = tweet.retweeted_status.favorite_count
        data.append(
            [
                tweet.created_at,
                tweet.user.screen_name,
                tweet.full_text,
                tweet.coordinates,
                tweet.user,
                tweet.retweet_count,
                likes_count,  # Likes count for tweet or retweet
                tweet.lang,
            ]
        )

    df = pd.DataFrame(data, columns=columns)

    df.to_csv(f"{game} Tweets.csv")


for game in game_list:
    """Loop Though all of the games"""
    print(f"Searching tweets for {game}")
    search_tweets(game)
