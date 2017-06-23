from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


print(TextBlob("Hummus is amazingly awesome. Hummus is terrible.").sentiment)
print(TextBlob("Hummus is amazingly awesome. Hummus is terrible.", analyzer=NaiveBayesAnalyzer()).sentiment.classification)
print(TextBlob("Hummus is amazingly awesome. Hummus is terrible.", analyzer=NaiveBayesAnalyzer()).sentiment.p_pos)