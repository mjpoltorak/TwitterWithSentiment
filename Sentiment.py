import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

import sys

keyWord = input("Please enter a keyword (No spaces allowed): ")





class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        try:
            # decode json
            dict_data = json.loads(data)

            if 'text' in dict_data:
                # pass tweet into TextBlob
                tweet = TextBlob(dict_data["text"])
                print(tweet)

                # output sentiment polarity
                print(tweet.sentiment)

                # determine if sentiment is positive, negative, or neutral
                if tweet.sentiment.polarity < 0:
                    sentiment = "negative"
                elif tweet.sentiment.polarity == 0:
                    sentiment = "neutral"
                else:
                    sentiment = "positive"

                # output sentiment
                print(sentiment)
            else:
                print("HELP! NO TEXT")

            return True

        except KeyboardInterrupt:
            print()
            print()
            print("Goodbye :)")
            sys.exit(0)  # or 1, or whatever

    # on failure
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    consumer_key = 'P1TpnobTYWuLnAWSPOIpp5FDj'
    consumer_secret = 'oAZxnwVbEEKYivhzWLYNGvmIXBdxZxUWcc7CGIaCWhjNQMW80a'

    access_token = '2936445550-sQGC6DPNjI8wwRmUKJM7W8vxa6jSOElNn0e3Xga'
    access_token_secret = 'bKQa1SCAu6vd9hKJGw30NnPYlzQ4NegT9afubYuYRmD5w'

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    stream.filter(languages=["en"], track=[keyWord])