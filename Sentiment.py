import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import sys
import signal

keyWord = input("Please enter a keyword (No spaces allowed): ")

#TODO:

def sigint_handler(signum, frame):
    print()
    print()
    sys.exit("Goodbye")
    return


signal.signal(signal.SIGINT, sigint_handler)

class TweetStreamListener(StreamListener):
    # on success
    def on_data(self, data):
        import psycopg2

        conn = psycopg2.connect("dbname='postgres' user='postgres' host='dev-datafactory-postgresql.csodrrohkuas.us-east-1.rds.amazonaws.com' password='sbterminal'")
        cur = conn.cursor()
        # cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        # print(cur.fetchall())

        try:
            # decode json
            dict_data = json.loads(data)

            if 'text' in dict_data:
                # pass tweet into TextBlob
                tweetS = TextBlob(dict_data["text"])
                handle = '@%s' % (dict_data['user']['screen_name'])
                tweet = '%s' % dict_data['text'].encode('ascii', 'ignore')
                time = '%s' % dict_data['created_at']
                tweet = tweet[2:]
                tweet = tweet[:-1]
                tweet = tweet.replace("'", "")
                #print(handle)
                #print(tweet)

                # output sentiment polarity
                polarity = tweetS.sentiment.polarity
                #print(polarity)

                # determine if sentiment is positive, negative, or neutral
                if tweetS.sentiment.polarity < 0:
                    sentiment = "negative"
                elif tweetS.sentiment.polarity == 0:
                    sentiment = "neutral"
                else:
                    sentiment = "positive"

                # output sentiment
                #print(sentiment)

                insert = f"INSERT INTO testing VALUES ('{tweet}', '{handle}', '{polarity}', '{sentiment}', '{time}');"
                print(insert)
                cur.execute(insert)
                conn.commit()

            else:
                print("HELP! NO TEXT")

            return True

        except KeyboardInterrupt:
            print()
            print()
            sys.exit("Goodbye :)")  # or 1, or whatever
            return True

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

    # search twitter for keyword
    stream.filter(languages=["en"], track=[keyWord])