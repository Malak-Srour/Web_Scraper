from flask import Flask, jsonify, request
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



######   ERROR   ######
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



# Route for getting articles by keyword/<keyword>-->Returns a list of articles that contain a specific keyword.
@app.route('/articles_by_keyword/<keyword>', methods=['GET'])
def articles_by_keyword(keyword):
    # Search for articles that contain the keyword in their 'keywords' field
    query = {"keywords": keyword}
    articles = collection.find(query)

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles]
    return jsonify(formatted_result)


# Route for getting articles by author/<author_name>-->Returns all articles written by a specific author
@app.route('/articles_by_author/<author_name>', methods=['GET'])
def articles_by_author(author_name):
    # Decode the URL-encoded author name
    author_name = request.view_args['author_name']
    # Search for articles that have the specified author
    query = {"author": author_name}
    articles = collection.find(query)

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles]
    return jsonify(formatted_result)


# Route for getting articles by author/
@app.route('/article_details/<postid>', methods=['GET'])
def article_details(postid):
    # Search for an article that matches the given postid
    article = collection.find_one({"postid": postid})

    if article:
        # Format and return the article details
        article_details = {
            "URL": article.get("url", "No URL available"),
            "Title": article.get("title", "No title available"),
            "Keywords": article.get("keywords", []),
        }
        return jsonify(article_details)
    else:
        return jsonify({"error": "Article not found"}), 404


# Route for getting articles with video -->Returns a list of articles that contain a video (where video_duration is not null).
@app.route('/articles_with_video', methods=['GET'])
def articles_with_video():
    # Search for articles that have a non-null video_duration
    articles = collection.find({"video_duration": {"$ne": None}})

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles if "title" in article]
    return jsonify(formatted_result)




# Route for getting articles by publication year
@app.route('/articles_by_year/<int:year>', methods=['GET'])
def articles_by_year(year):
    # Define the pipeline to match articles from the specified year
    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$eq": [{"$year": {"$dateFromString": {"dateString": "$published_time"}}}, year]
                }
            }
        },
        {
            "$group": {
                "_id": year,
                "article_count": {"$sum": 1}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    if result:
        return jsonify({f"{year}": f"{result[0]['article_count']} articles"})
    else:
        return jsonify({f"{year}": "0 articles"}), 404


# Route for getting the top 10 longest articles by word count
@app.route('/longest_articles', methods=['GET'])
def longest_articles():
    pipeline = [
        {"$sort": {"word_count": -1}},  # Sort articles by word count in descending order
        {"$limit": 10}  # Limit the result to the top 10 articles
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to include only the title and word count
    formatted_result = [
        f'"{article["title"]}" ({article["word_count"]} words)'
        for article in result
    ]

    return jsonify(formatted_result)


# Route for getting the top 10 shortest articles by word count
@app.route('/shortest_articles', methods=['GET'])
def shortest_articles():
    pipeline = [
        {"$sort": {"word_count": 1}},  # Sort articles by word count in ascending order
        {"$limit": 10}  # Limit the result to the top 10 articles
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to include only the title and word count
    formatted_result = [
        f'"{article["title"]}" ({article["word_count"]} words)'
        for article in result
    ]

    return jsonify(formatted_result)


# Route for getting the top 10 shortest articles by word count (greater than one word)
@app.route('/shortest_articles_not_zero', methods=['GET'])
def shortest_articles_not_zero():
    pipeline = [
        {"$match": {"word_count": {"$gt": 1}}},  # Filter out articles with a word count of 1 or less
        {"$sort": {"word_count": 1}},  # Sort articles by word count in ascending order
        {"$limit": 10}  # Limit the result to the top 10 articles
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to include only the title and word count
    formatted_result = [
        f'"{article["title"]}" ({article["word_count"]} words)'
        for article in result
    ]

    return jsonify(formatted_result)


# Route for getting articles grouped by the number of keywords
@app.route('/articles_by_keyword_count', methods=['GET'])
def articles_by_keyword_count():
    pipeline = [
        # Project the number of keywords in each article
        {
            "$project": {
                "keyword_count": {"$size": {"$split": ["$keywords", ","]}}
            }
        },
        # Group by the keyword count and count the number of articles
        {
            "$group": {
                "_id": "$keyword_count",
                "article_count": {"$sum": 1}
            }
        },
        # Sort by keyword count in ascending order (optional)
        {"$sort": {"_id": 1}}
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to display the keyword count and number of articles
    formatted_result = {f"{item['_id']} keywords": f"{item['article_count']} articles" for item in result}

    return jsonify(formatted_result)


if __name__ == '__main__':
    app.run(debug=True)
