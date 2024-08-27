from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta


app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]


@app.route('/')
def index():
    return render_template('index.html')



# 1- Route for getting top keywords
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



# 2- Route for getting top authors
@app.route('/top_authors', methods=['GET'])
def top_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)



# 3- Articles by Date --> Returns the number of articles published on each date, sorted by date.
@app.route('/articles_by_date', methods=['GET'])
def articles_by_date():
    pipeline = [
        {"$project": {
            "date": {"$dateToString": {"format": "%Y-%m-%d", "date": {"$toDate": "$published_time"}}}
        }},
        {"$group": {"_id": "$date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = list(collection.aggregate(pipeline))
    formatted_results = {f"{result['_id']}": f"{result['count']} articles" for result in results}
    return jsonify(formatted_results)




# 4- Route for getting articles by word count
@app.route('/articles_by_word_count', methods=['GET'])
def articles_by_word_count():
    pipeline = [
        {"$group": {"_id": "$word_count", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}  # Sort by word count in ascending order
    ]
    results = list(collection.aggregate(pipeline))
    # Formatting the result for better clarity in output as specified
    formatted_results = {f"{result['_id']} words": f"{result['count']} articles" for result in results}
    return jsonify(formatted_results)



# 5- Route for getting articles by language
@app.route('/articles_by_language', methods=['GET'])
def articles_by_language():
    pipeline = [
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}  # Sorting by count in descending order
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item['_id']: item['count'] for item in result})


# 6-



# 7- Route for getting articles by recent articles
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



# 8- Route for getting articles by keyword/<keyword>-->Returns a list of articles that contain a specific keyword.
@app.route('/articles_by_keyword/<keyword>', methods=['GET'])
def articles_by_keyword(keyword):
    # Search for articles that contain the keyword in their 'keywords' field
    query = {"keywords": keyword}
    articles = collection.find(query)

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles]
    return jsonify(formatted_result)


# 9- Route for getting articles by author/<author_name>-->Returns all articles written by a specific author
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



# 10-



# 11- Route for getting articles by author/
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


# 12- Route for getting articles with video -->Returns a list of articles that contain a video (where video_duration is not null).
@app.route('/articles_with_video', methods=['GET'])
def articles_with_video():
    # Search for articles that have a non-null video_duration
    articles = collection.find({"video_duration": {"$ne": None}})

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles if "title" in article]
    return jsonify(formatted_result)




# 13- Route for getting articles by publication year
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


### edit ###
# 14- Route for getting the top 10 longest articles by word count
@app.route('/longest_articles', methods=['GET'])
def longest_articles():
    pipeline = [
        {"$sort": {"word_count": -1}},  # Sort articles by word count in descending order
        {"$limit": 10},  # Limit the result to the top 10 articles
        {"$project": {"title": 1, "word_count": 1, "_id": 1}}  # Include title, word count, and _id
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to include the title, word count, and _id
    formatted_result = [
        f'Article ID: {article["_id"]}, "{article["title"]}" ({article["word_count"]} words)'
        for article in result
    ]

    return jsonify(formatted_result)


# 15- Route for getting the top 10 shortest articles by word count
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


# 16- Route for getting articles grouped by the number of keywords
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


# 17- Route for getting articles that have a thumbnail image
@app.route('/articles_with_thumbnail', methods=['GET'])
def articles_with_thumbnail():
    # Find articles where the thumbnail field is not null or empty
    query = {"thumbnail": {"$ne": None, "$ne": ""}}
    articles = collection.find(query)

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles if "title" in article]

    return jsonify(formatted_result)


# 18- Route for getting articles that were updated after publication
@app.route('/articles_updated_after_publication', methods=['GET'])
def articles_updated_after_publication():
    # Find articles where the last_updated time is after the published_time
    query = {
        "$expr": {
            "$gt": ["$last_updated", "$published_time"]
        }
    }
    articles = collection.find(query)

    # Format the response to include only the titles of the articles
    formatted_result = [article["title"] for article in articles if "title" in article]

    return jsonify(formatted_result)



# 19-



# 20- Route for getting the most popular keywords from day X and after
@app.route('/popular_keywords_last_<int:days>_days', methods=['GET'])
def popular_keywords_last_X_days(days):
    # Calculate the start date, X days ago from today
    start_date = datetime.now() - timedelta(days=days)

    # Define the pipeline to filter articles and aggregate keyword counts
    pipeline = [
        # Match articles published on or after the start date
        {
            "$match": {
                "published_time": {"$gte": start_date.isoformat()}
            }
        },
        # Unwind the keywords array
        {"$unwind": "$keywords"},
        # Group by keywords and count occurrences
        {
            "$group": {
                "_id": "$keywords",
                "count": {"$sum": 1}
            }
        },
        # Sort by count in descending order
        {"$sort": {"count": -1}},
        # Limit to the top 10 most frequent keywords
        {"$limit": 10}
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to display the keyword and its occurrence count
    formatted_result = [f'"{item["_id"]}" ({item["count"]} occurrences)' for item in result]

    return jsonify(formatted_result)



# 21- Route for getting the number of articles published in a specific month and year
@app.route('/articles_by_month/<int:year>/<int:month>', methods=['GET'])
def articles_by_month(year, month):
    try:
        # Parse the year and month into a datetime object representing the first day of that month
        start_date = datetime(year, month, 1)

        # Calculate the first day of the next month to use as an upper bound
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

    except ValueError:
        return jsonify({"error": "Invalid year or month provided."}), 400

    # Define the pipeline to match articles within the specified month and count them
    pipeline = [
        {
            "$match": {
                "published_time": {"$gte": start_date.isoformat(), "$lt": end_date.isoformat()}
            }
        },
        {
            "$group": {
                "_id": None,
                "article_count": {"$sum": 1}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result
    if result:
        month_name = start_date.strftime("%B")
        formatted_result = f"{month_name} {year} ({result[0]['article_count']} articles)"
    else:
        formatted_result = f"{start_date.strftime('%B')} {year} (0 articles)"

    return jsonify(formatted_result)


# 22- Route for getting articles within a specific word count range
@app.route('/articles_by_word_count_range/<int:min>/<int:max>', methods=['GET'])
def articles_by_word_count_range(min, max):
    # Define the pipeline to match articles within the specified word count range
    pipeline = [
        {
            "$match": {
                "word_count": {"$gte": min, "$lte": max}
            }
        },
        {
            "$group": {
                "_id": None,
                "article_count": {"$sum": 1}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result
    if result and result[0]['article_count'] > 0:
        formatted_result = f"Articles between {min} and {max} words ({result[0]['article_count']} articles)"
    else:
        formatted_result = f"Articles between {min} and {max} words (0 articles)"

    return jsonify(formatted_result)


# 23- Route for getting articles with a specific number of keywords
@app.route('/articles_with_specific_keyword_count/<int:count>', methods=['GET'])
def articles_with_specific_keyword_count(count):
    # Define the pipeline to match articles with the exact keyword count
    pipeline = [
        # Project the number of keywords in each article
        {
            "$project": {
                "keyword_count": {"$size": {"$split": ["$keywords", ","]}}
            }
        },
        # Match articles with the specific keyword count
        {
            "$match": {
                "keyword_count": count
            }
        },
        # Group by the keyword count and count the number of articles
        {
            "$group": {
                "_id": None,
                "article_count": {"$sum": 1}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result
    if result and result[0]['article_count'] > 0:
        formatted_result = f"Articles with exactly {count} keywords ({result[0]['article_count']} articles)"
    else:
        formatted_result = f"Articles with exactly {count} keywords (0 articles)"

    return jsonify(formatted_result)


# 24- Route for getting articles published on a specific date
@app.route('/articles_by_specific_date/<string:date>', methods=['GET'])
def articles_by_specific_date(date):
    try:
        # Parse the date from the string (expected format: YYYY-MM-DD)
        specific_date = datetime.strptime(date, "%Y-%m-%d")

        # Define the start and end times for the specific date
        start_date = specific_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = specific_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    # Define the pipeline to match articles within the specified date range
    pipeline = [
        {
            "$match": {
                "published_time": {"$gte": start_date.isoformat(), "$lte": end_date.isoformat()}
            }
        },
        {
            "$group": {
                "_id": None,
                "article_count": {"$sum": 1}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result
    if result and result[0]['article_count'] > 0:
        formatted_result = f"Articles published on \"{date}\" ({result[0]['article_count']} articles)"
    else:
        formatted_result = f"Articles published on \"{date}\" (0 articles)"

    return jsonify(formatted_result)



# 25-
@app.route('/articles_containing_text/<text>', methods=['GET'])
def articles_containing_text(text):
    # Fetch all documents (not recommended for large collections)
    documents = list(collection.find({}, {"title": 1, "description": 1, "full_text": 1, "url": 1, "_id": 0}))
    # Filter documents to find those containing the text
    results = [
        doc for doc in documents
        if text.lower() in doc.get('title', '').lower() or
           text.lower() in doc.get('description', '').lower() or
           text.lower() in doc.get('full_text', '').lower()
    ]

    if not results:
        return jsonify({"message": f"No articles containing '{text}' found"}), 404
    return jsonify(results)



# 26- Route for getting articles with more than a specified number of words
@app.route('/articles_with_more_than/<int:word_count>', methods=['GET'])
def articles_with_more_than(word_count):
    # Define the pipeline to match articles with more than the specified word count
    pipeline = [
        {
            "$match": {
                "word_count": {"$gt": word_count}
            }
        },
        {
            "$group": {
                "_id": None,
                "article_count": {"$sum": 1}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result
    if result and result[0]['article_count'] > 0:
        formatted_result = f"Articles with more than {word_count} words ({result[0]['article_count']} articles)"
    else:
        formatted_result = f"Articles with more than {word_count} words (0 articles)"

    return jsonify(formatted_result)



# 27-
@app.route('/articles_by_specific_date/<date>', methods=['GET'])
def get_articles_by_date(date, articles_collection=None):
    # Convert date string to datetime object
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Calculate the start and end of the day
    start_of_day = datetime(date.year, date.month, date.day)
    end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)

    # Query MongoDB for articles published within the given day
    query = {
        "published_time": {
            "$gte": start_of_day.isoformat(),
            "$lte": end_of_day.isoformat()
        }
    }
    articles = list(articles_collection.find(query))

    # Prepare response data
    if articles:
        article_count = len(articles)
        response_data = {
            f'Articles published on "{date.strftime("%Y-%m-%d")}"': f"{article_count} articles"
        }
    else:
        response_data = {
            f'Articles published on "{date.strftime("%Y-%m-%d")}"': "No articles found"
        }

    return jsonify(response_data)



# 28- articles_last_X_hours --> Returns a list of articles published in the last X hours.
import pytz

@app.route('/articles_last_X_hours/<int:x>', methods=['GET'])
def articles_last_x_hours(x):
    # Calculate the datetime X hours ago
    utc_now = datetime.now(pytz.utc)
    x_hours_ago = utc_now - timedelta(hours=x)

    # Query to find articles published in the last X hours
    query = {
        "published_time": {"$gte": x_hours_ago.isoformat()}
    }
    results = list(collection.find(query, {"title": 1, "published_time": 1, "_id": 0}))

    # Formatting results for response
    formatted_results = [
        f"{doc['title']} (Published within the last {x} hours)"
        for doc in results
    ]
    if not results:
        return jsonify({"message": f"No articles published in the last {x} hours found"}), 404
    return jsonify(formatted_results)



# 29-
@app.route('/articles_by_title_length', methods=['GET'])
def articles_by_title_length():
    # Query all articles
    articles = collection.find({}, {"title": 1})  # Project to only include the title field

    # Initialize a dictionary to count articles by title length
    title_length_count = {}

    # Count the number of words in each title and update the dictionary
    for article in articles:
        if 'title' in article:
            word_count = len(article['title'].split())  # Split title into words and count
            if word_count in title_length_count:
                title_length_count[word_count] += 1
            else:
                title_length_count[word_count] = 1

    # Format the response to include the word count and number of articles
    response_data = {f'Titles with {length} words': f'{count} articles' for length, count in title_length_count.items()}

    return jsonify(response_data)



# 30-


if __name__ == '__main__':
    app.run(debug=True)
