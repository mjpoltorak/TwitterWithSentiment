import json
from tweepy.streaming import StreamListener
from textblob.sentiments import NaiveBayesAnalyzer
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
                tweet2 = TextBlob(dict_data["text"])
                tweet = TextBlob(dict_data["text"], analyzer=NaiveBayesAnalyzer())
                print(tweet)

                # output sentiment polarity
                print(tweet.sentiment)
                print(tweet2.sentiment)
                # print(tweet.sentiment)

                # determine if sentiment is positive, negative, or neutral
                # if tweet.sentiment.polarity < 0:
                #     sentiment = "negative"
                # elif tweet.sentiment.polarity == 0:
                #     sentiment = "neutral"
                # else:
                #     sentiment = "positive"

                # output sentiment
                # print(sentiment)
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
    consumer_key = 'sKLz5yvDnmIr40yicNGBMBTax'
    consumer_secret = '1i1U513KAjszpJmYX02QUMHOIJpDishS8MoDJDdEvRuahSGe42'

    access_token = '870293629742567425-MbTugzaAx1YsbVUwHS8aiKPNCOLk7CX'
    access_token_secret = 'Hmr6iW42sFjXArT0Y1H7uenoxXGhAorgWqLcUPIcvhVVd'

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    stream.filter(languages=["en"], track=[keyWord])