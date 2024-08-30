from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta


app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]


#1
@app.route('/generateCloud')
def generateCloud():
    return render_template('word_cloud,top_keywords.html')

#2
@app.route('/top_authors_chart')
def top_authors_chart():
    return render_template('2-bar-top_authors.html')

#3
@app.route('/by_date')
def by_date():
    return render_template('line_graph,articles_by_date.html')

#4
@app.route('/by_word_count')
def by_word_count():
    return render_template('4-hist,articles_by_word_count.html')

#5
@app.route('/by_lang')
def by_lang():
    return render_template('5-pie_chart_by_lang.html')

#6

#7
@app.route('/by_recent_articles')
def by_recent_articles():
    return render_template('7-table_reent_articles.html')

#8
#9

#10
@app.route('/by_top_classes')
def by_top_classes():
    return render_template('10-semi_circle_pie_chart_top_classes.html')

#11

#12
@app.route('/by_video')
def by_video():
    return render_template('12-bar_chart_with_video.html')

#13

#14
@app.route('/by_longest_articles')
def by_longest_articles():
    return render_template('14-bar-longest_articles.html')

#15
@app.route('/by_shortest_articles_zero')
def by_shortest_articles_zero():
    return render_template('15-bar-shortest_articles_zero.html')

@app.route('/by_shortest_articles')
def by_shortest_articles():
    return render_template('15-bar-shortest_articles.html')

#16
@app.route('/by_keyword_count')
def keyword_count():
    return render_template('16-hist-keyword_count.html')

#17
@app.route('/by_thumbnail')
def by_thumbnail():
    return render_template('17-pie-thumbnail.html')

#18
@app.route('/updated_after_pub')
def updated_after_pub():
    return render_template('18-bar-updated_after_pub.html')


#19
#20
@app.route('/last_x_days')
def last_x_days():
    return render_template('20-line-chart-popular_in_x_days.html')


#21
@app.route('/by_month')
def by_month():
    return render_template('21-bar-articles_by_month.html')

#22
@app.route('/word_count_range')
def word_count_range():
    return render_template('22-hist-word_count_range.html')


#23
#24
#25
#26
@app.route('/more_than_n_words')
def more_than_n_words():
    return render_template('26-more_than_word_count.html')

#27
#28
#29
@app.route('/length_of_title')
def length_of_title():
    return render_template('29-spiral-bar-chart-length_of_title.html')


#30

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
    jsonp_callback = request.args.get('callback')
    if jsonp_callback:
        content = f'{jsonp_callback}({jsonify(result).get_data(as_text=True)})'
        return app.response_class(content, mimetype='application/javascript')
    else:
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


# 6- Route for articles by classes
@app.route('/articles_by_classes', methods=['GET'])
def get_articles_by_classes():
    # MongoDB aggregation pipeline
    pipeline = [
        {"$unwind": "$classes"},  # Unwind the classes array
        {"$group": {
            "_id": "$classes.value",  # Group by the value in the classes array
            "count": {"$sum": 1}  # Count the number of occurrences
        }},
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Format the result for better readability
    response = {item['_id']: item['count'] for item in result}

    return jsonify(response)


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
def get_articles_by_keyword(keyword):
    # MongoDB query to find articles that contain the specific keyword in the keywords array
    query = {"keywords": keyword}
    projection = {"_id": 0, "title": 1, "url": 1, "description": 1}   # Adjust projection to return fields you want

    # Find all matching articles
    articles = list(collection.find(query, projection))

    # Return the list of titles
    return jsonify(articles)


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
@app.route('/top_classes', methods=['GET'])
def get_top_classes():
    # MongoDB aggregation pipeline
    pipeline = [
        {"$unwind": "$classes"},  # Unwind the classes array
        {"$group": {
            "_id": "$classes.value",  # Group by the value in the classes array
            "count": {"$sum": 1}  # Count the number of occurrences
        }},
        {"$sort": {"count": -1}},  # Sort by count in descending order
        {"$limit": 10}  # Limit to top 10 classes
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Format the result for better readability
    response = {item['_id']: item['count'] for item in result}

    return jsonify(response)


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
def get_articles_with_video():
    # MongoDB query to find articles where video_duration is not null
    query_with_video = {"video_duration": {"$ne": None}}
    projection = {"_id": 0, "postid": 1, "url": 1}  # Include postid and URL in the projection

    # Find all matching articles with videos
    articles_with_video = list(collection.find(query_with_video, projection))

    # Count the number of articles with videos
    count_with_video = collection.count_documents(query_with_video)

    # MongoDB query to find articles where video_duration is null
    query_without_video = {"video_duration": None}

    # Count the number of articles without videos
    count_without_video = collection.count_documents(query_without_video)

    # Prepare the response
    response = {
        "articles_with_video": articles_with_video,
        "count_with_video": count_with_video,
        "count_without_video": count_without_video
    }

    # Return the response as JSON
    return jsonify(response)





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
def get_articles_by_keyword_count():
    # MongoDB aggregation pipeline
    pipeline = [
        {"$project": {"keyword_count": {"$size": "$keywords"}}},  # Calculate the number of keywords
        {"$group": {
            "_id": "$keyword_count",  # Group by the keyword count
            "count": {"$sum": 1}  # Count the number of articles in each group
        }},
        {"$sort": {"_id": 1}}  # Optional: Sort by keyword count
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Format the result for better readability
    response = {f"{item['_id']} keywords": item['count'] for item in result}

    return jsonify(response)


# 17- Route for getting articles that have a thumbnail image
@app.route('/articles_with_thumbnail', methods=['GET'])
def articles_with_thumbnail():
    # Find articles where the thumbnail field is not null or empty
    query = {"thumbnail": {"$ne": None, "$ne": ""}}
    articles_with_thumbnail = list(collection.find(query, {"title": 1, "_id": 0}))

    # Count the number of articles with a thumbnail
    with_thumbnail_count = len(articles_with_thumbnail)

    # Count the number of articles without a thumbnail
    without_thumbnail_count = collection.count_documents({"$or": [{"thumbnail": None}, {"thumbnail": ""}]})

    # Extract the titles of the articles
    titles = [article["title"] for article in articles_with_thumbnail if "title" in article]

    # Add the counts to the response
    result = {
        "titles": titles,
        "summary": {
            "With Thumbnail": with_thumbnail_count,
            "Without Thumbnail": without_thumbnail_count
        }
    }

    return jsonify(result)


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
@app.route('/articles_by_coverage/<coverage>', methods=['GET'])
def get_articles_by_coverage(coverage):
    # MongoDB query to find articles where classes array contains the specified coverage
    query = {"classes": {"$elemMatch": {"mapping": "coverage", "value": coverage}}}
    projection = {"_id": 0, "title": 1}  # Adjust projection to return the fields you want

    # Find all matching articles
    articles = list(collection.find(query, projection))

    # Extract just the titles for the response
    titles = [article["title"] for article in articles]

    # Return the list of titles
    return jsonify(titles)


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
def get_articles_with_specific_keyword_count(count):
    # MongoDB query to find articles with exactly the specified number of keywords
    query = {"$expr": {"$eq": [{"$size": "$keywords"}, count]}}
    projection = {"_id": 0, "title": 1, "keywords": 1}  # Include both title and keywords

    # Find all matching articles
    articles = list(collection.find(query, projection))

    # Return the list of titles and keywords
    return jsonify(articles)



# 24- Route for getting articles published on a specific date
# example: 2024-08-10
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
@app.route('/articles_grouped_by_coverage', methods=['GET'])
def get_articles_grouped_by_coverage():
    # MongoDB aggregation pipeline
    pipeline = [
        {"$unwind": "$classes"},  # Unwind the classes array
        {"$match": {"classes.mapping": "coverage"}},  # Match only classes with mapping 'coverage'
        {"$group": {
            "_id": "$classes.value",  # Group by the 'value' field where 'mapping' is 'coverage'
            "count": {"$sum": 1}  # Count the number of articles in each group
        }}
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Format the result without sorting
    response = {f"Coverage on {item['_id']}": item['count'] for item in result}

    return jsonify(response)



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
    # Query all articles and project only the title field
    articles = collection.find({}, {"title": 1})

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

    # Sort the dictionary by the word count (key) and create a sorted list of tuples
    sorted_title_length_count = sorted(title_length_count.items())

    # Format the data for the chart
    chart_data = [{"category": f"{length} words", "value": count} for length, count in sorted_title_length_count]

    return jsonify(chart_data)





# 30-


if __name__ == '__main__':
    app.run(debug=True)
