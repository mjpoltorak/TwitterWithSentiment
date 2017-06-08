# TwitterWithSentiment

# Sentiment.py
This program gets live tweets as they come in. The twitter API, tweepy, used here is much more efficient and effective as a solution as opposed to HTML parsing (one of my previous repositories). In addition to fetching live tweets, this program also analyzes the sentiment of the tweet (positive or negative). This script also live streams the incoming data into the postgres database.
Necessary libraries include: json, tweepy, textblob, sys

#PopulateDatabse.py
Please do not run this file as you will add rows to the current database which has been successfully filled. The script populates a database with all NYSE and Nasdaq tickers and their corresponding company names.
