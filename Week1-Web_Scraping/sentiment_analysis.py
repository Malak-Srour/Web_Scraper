# sentiment_analysis.py

from pymongo import MongoClient
from textblob import TextBlob

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]

# Function to determine sentiment and polarity
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # Get the polarity value
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return sentiment, polarity

# Update each article with sentiment and polarity
for article in collection.find():
    sentiment, polarity = get_sentiment(article['full_text'])
    collection.update_one(
        {'_id': article['_id']},
        {'$set': {'sentiment': sentiment, 'sentiment_number': polarity}}
    )

print("Sentiment analysis completed and stored in MongoDB.")
