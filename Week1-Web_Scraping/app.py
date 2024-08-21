from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]



# Route for getting top keywords
@app.route('/top_keywords', methods=['GET'])
def top_keywords():
    pipeline = [
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

# Route for getting top authors
@app.route('/top_authors', methods=['GET'])
def top_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)



# Route for getting articles by word count
@app.route('/articles_by_word_count', methods=['GET'])
def articles_by_word_count():
    pipeline = [
        {"$group": {"_id": "$word_count", "article_count": {"$sum": 1}}},
        {"$sort": {"$word_count": -1}}  # Sorting by the number of articles in descending order
    ]
    result = list(collection.aggregate(pipeline))
    # Format the result to make it more readable
    formatted_result = {f"{item['_id']} words": f"{item['article_count']} articles" for item in result}
    return jsonify(formatted_result)



# Route for getting articles by language
@app.route('/articles_by_language', methods=['GET'])
def articles_by_language():
    pipeline = [
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}  # Sorting by count in descending order
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item['_id']: item['count'] for item in result})


# Route for getting articles by recent articles
@app.route('/recent_articles', methods=['GET'])
def recent_articles():
    pipeline = [
        {"$sort": {"published_time": -1}},  # Sorting by published_time in descending order
        {"$limit": 10}  # Limiting to the 10 most recent articles
    ]
    result = list(collection.aggregate(pipeline))
    formatted_result = [
        {"title": article["title"], "published_date": article["published_time"]}
        for article in result
    ]
    return jsonify(formatted_result)

# Route for getting articles by keywords
@app.route('/articles_by_keyword/<keyword>', methods=['GET'])
def articles_by_keyword(keyword):
    # Search for articles that contain the keyword in their 'keywords' field
    query = {"keywords": keyword}
    articles = collection.find(query)

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles]
    return jsonify(formatted_result)



if __name__ == '__main__':
    app.run(debug=True)
