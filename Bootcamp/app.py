from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from pymongo import MongoClient
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'super_secret_key'


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]
users_collection = db["users"]

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Hash the password securely using pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Store the user in the database
        users_collection.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password
        })

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email exists in the database
        user = users_collection.find_one({"email": email})

        if user:
            # Check if the password is correct
            if check_password_hash(user['password'], password):
                # Store user info in session
                session['user_id'] = str(user['_id'])
                session['first_name'] = user['first_name']
                session['email'] = user['email']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))  # Redirect to some dashboard or homepage
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('Email not found. Please register first.', 'danger')

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))



@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', title="Article Dashboard")
    else:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

@app.route('/authors_dashboard', methods=['GET'])
def authors_dashboard():
    # Render the HTML template for the top authors chart
    return render_template('authorsdashboard.html', title="Authors")

@app.route('/keywords_dashboard', methods=['GET'])
def keywords_dashboard():
    # Render the HTML template for the top authors chart
    return render_template('keywords_dashboard.html', title="Keywords")

@app.route('/date_time_dashboard', methods=['GET'])
def date_time_dashboard():
    # Render the HTML template for the top authors chart
    return render_template('date_time_dashboard.html', title="Date and Time")

@app.route('/word_count_dashboard', methods=['GET'])
def word_count_dashboard_chart():
    # Render the HTML template for the top authors chart
    return render_template('word_count_dashboard.html', title="Word Count")

@app.route('/classes_dashboard', methods=['GET'])
def classes_dashboard_chart():
    # Render the HTML template for the top authors chart
    return render_template('classes_dashboard.html', title="Classes")

@app.route('/sentiment_analysis_dashboard', methods=['GET'])
def sentiment_dashboard_chart():
    # Render the HTML template for the top authors chart
    return render_template('sentiment_dashboard.html', title="Sentiment Analysis")





# 1
@app.route('/top_authors_chart', methods=['GET'])
def top_authors_chart():
    # Render the HTML template for the top authors chart
    return render_template('top_authors.html', title="Top Authors")

# 2
@app.route('/articles_by_word_count_chart')
def articles_by_word_count_chart():
    return render_template('articles_by_word_count.html', title="Articles by Word Count")

# 3
@app.route('/articles_by_language_chart')
def articles_by_language_chart():
    return render_template('articles_by_language.html', title="Articles by Language")

# 4
@app.route('/recent_articles_chart')
def recent_articles_chart():
    return render_template('recent_articles.html', title="Recent Articles")

# 5
@app.route('/articles_with_video_chart')
def articles_with_video_chart():
    return render_template('articles_with_video.html', title="Articles with and without Videos")

# 6
@app.route('/longest_articles_chart')
def longest_articles_chart():
    return render_template('longest_articles.html', title="Longest Articles by Word Count")

# 7
@app.route('/shortest_articles_chart')
def shortest_articles_chart():
    return render_template('shortest_articles.html', title="Shortest Articles (Non-Zero Word Count)")

#8
@app.route('/articles_by_keyword_count_chart')
def articles_by_keyword_count_chart():
    return render_template('articles_by_keyword_count.html', title="Articles by Keyword Count")

# 9
@app.route('/articles_by_thumbnail_chart')
def articles_by_thumbnail_chart():
    return render_template('articles_by_thumbnail.html', title="Articles by Thumbnail Presence")

#10
@app.route('/articles_updated_chart')
def articles_updated_chart():
    return render_template('articles_updated.html', title="Articles Updated After Publication")

# 11
@app.route('/popular_keywords_chart')
def popular_keywords_chart():
    return render_template('popular_keywords.html', title="Most Popular Keywords in the Last X Days")

# 12
@app.route('/articles_by_month')
def articles_by_month():
    return render_template('articles_by_month.html', title="Articles by Published Month")

#13
@app.route('/articles_by_word_count_range')
def articles_by_word_count_range():
    return render_template('articles_by_word_count_range.html', title="Articles by Word Count Range")

# 14
@app.route('/articles_with_more_than')
def articles_with_more_than():
    return render_template('articles_with_more_than.html', title="Articles with More than N Words")

# 15
@app.route('/articles_by_title_length_chart')
def articles_by_title_length_chart():
    return render_template('articles_by_title_length.html', title="Articles by Title Length")

# 16
@app.route('/articles_by_date_chart')
def articles_by_date_chart():
    return render_template('articles_by_date.html', title="Articles by Date")

# 17
@app.route('/top_keywords_chart')
def top_keywords_wordcloud():
    return render_template('top_keywords_wordcloud.html', title="Top Keywords Word Cloud")

# 18
@app.route('/articles_by_sentiment_chart', methods=['GET'])
def articles_by_sentiment_chart():
    return render_template('sentiment.html', title="Articles by Sentiment (Logarithmic)")

# 19
@app.route('/most_positive_articles_chart')
def most_positive_articles_chart():
    return render_template('sentiment_most_positive.html', title="Most Positive Articles")

# 20
@app.route('/most_negative_articles_chart')
def most_negative_articles_chart():
    return render_template('sentiment_most_negative.html', title="Most Negative Articles")

# 21
@app.route('/author_articles_chart')
def author_articles():
    return render_template('author_articles.html', title="Total Articles Written by a Specific Author")

# 22
@app.route('/articles_by_keyword_chart')
def articles_chart():
    return render_template('articles_by_keyword.html', title="Articles by Specific Keyword")

#23
@app.route('/entites_chart')
def entites_chart():
    return render_template('entities.html', title="Top Entities Force-Directed Bubble Chart")

#24
@app.route('/top_entites_chart')
def top_entites_chart():
    return render_template('top_entities.html', title="Top Entities Force-Directed Bubble Chart")

# 25
@app.route('/top_classes_chart')
def top_classes_chart():
    return render_template('top_classes.html', title="Top Classes")

# 26
@app.route('/last_x_hours_chart')
def last_x_hours():
    return render_template('last_x_hours.html', title="Last X Hours")







# 1
@app.route('/top_authors_data', methods=['GET'])
def top_authors_data():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

# 2
@app.route('/articles_by_word_count', methods=['GET'])
def articles_by_word_count():
    pipeline = [
        {"$group": {"_id": "$word_count", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}  # Sort by word count in ascending order
    ]
    results = list(collection.aggregate(pipeline))

    # Format the result and filter out entries where category is "0"
    formatted_results = [
        {"category": str(result["_id"]), "value": result["count"]}
        for result in results if str(result["_id"]) != "0"  # Exclude category "0"
    ]

    return jsonify(formatted_results)



# 3
@app.route('/articles_by_language', methods=['GET'])
def articles_by_language():
    pipeline = [
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}  # Sorting by count in descending order
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item['_id']: item['count'] for item in result})

# 4
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

# 5
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

# 6
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

# 7
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

# 8
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

    # Format the result for better readability without the word "keywords"
    response = {str(item['_id']): item['count'] for item in result}

    return jsonify(response)


# 9
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

#10
@app.route('/articles_updated_after_publication', methods=['GET'])
def articles_updated_after_publication():
    # Total number of articles (assuming you know there are 10,000 articles)
    total_articles = 10000

    # Query to find articles where the last_updated time is after the published_time
    updated_query = {
        "$expr": {
            "$gt": ["$last_updated", "$published_time"]
        }
    }

    # Count of updated articles
    updated_count = collection.count_documents(updated_query)

    # Calculate the count of unupdated articles as 10000 - updated_count
    unupdated_count = total_articles - updated_count

    # Prepare the result
    result = {
        "updated_articles": updated_count,
        "unupdated_articles": unupdated_count
    }

    return jsonify(result)

# 11
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

# 12
@app.route('/articles_by_month/<int:year>/<int:month>', methods=['GET'])
def articles_by_month_route(year, month):
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

# 13
@app.route('/articles_by_word_count_range/<int:min>/<int:max>', methods=['GET'])
def articles_by_word_count_range_route(min, max):
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

# 14
@app.route('/articles_with_more_than/<int:word_count>', methods=['GET'])
def articles_with_more_than_route(word_count):
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

# 15
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

# 16
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

# 17
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

# 18
@app.route('/articles_by_sentiment_summary', methods=['GET'])
def get_articles_by_sentiment_summary():
    # List of sentiments
    sentiments = ['positive', 'neutral', 'negative']

    # Get total number of articles
    total_articles = collection.count_documents({})

    summary = []

    # Calculate count and percentage for each sentiment
    for sentiment in sentiments:
        count = collection.count_documents({'sentiment': sentiment})
        percentage = (count / total_articles) * 100 if total_articles > 0 else 0
        summary.append({'sentiment': sentiment, 'count': count, 'percentage': percentage})

    return jsonify(summary)


# 19
@app.route('/most_positive_articles', methods=['GET'])
def get_most_positive_articles():
    articles = collection.find().sort('sentiment_number', -1).limit(10)  # Sort by polarity in descending order (most positive)
    result = []
    for article in articles:
        result.append({
            'url': article['url'],
            'title': article['title'],
            'sentiment': article['sentiment'],
            'sentiment_number': article['sentiment_number']
        })
    return jsonify(result)

# 20
@app.route('/most_negative_articles', methods=['GET'])
def get_most_negative_articles():
    articles = collection.find().sort('sentiment_number', 1).limit(10)  # Sort by polarity in ascending order (most negative)
    result = []
    for article in articles:
        result.append({
            'category': article['title'],  # Use the title as the category (spiral label)
            'value': abs(article['sentiment_number'])  # Use the absolute sentiment number as value
        })
    return jsonify(result)

# 21
@app.route('/articles_by_author/<author_name>', methods=['GET'])
def articles_by_author(author_name):
    # Decode the URL-encoded author name
    author_name = request.view_args['author_name']

    # Search for articles that have the specified author
    query = {"author": author_name}
    articles = collection.find(query)

    # Extract titles and count the articles
    titles = [article["title"] for article in articles]
    count = len(titles)

    # Return a response with both the titles and the count
    return jsonify({"titles": titles, "count": count})

# 22
@app.route('/articles_by_keyword/<keyword>', methods=['GET'])
def get_articles_by_keyword(keyword):
    query = {"keywords": {"$regex": keyword, "$options": "i"}}
    projection = {"_id": 0, "title": 1, "url": 1, "description": 1}

    # Limit the results to 15 articles
    articles = list(collection.find(query, projection).limit(20))

    # Transform data into the required format for the chart
    chart_data = {
        "value": 0,
        "children": []
    }

    for article in articles:
        chart_data["children"].append({
            "name": article["title"],
            "value": 1,  # You can adjust this based on your logic
            "url": article["url"],
            "description": article["description"]
        })

    return jsonify(chart_data)

#23
@app.route('/entities', methods=['GET'])
def get_entities():
    search_query = request.args.get('query', '')  # Get the search term from the query string

    # MongoDB Aggregation query to group by 'entity' and 'type', and count occurrences
    pipeline = [
        {"$unwind": "$entities"},  # Unwind the 'entities' array
        {"$match": {
            "$or": [
                {"entities.entity": {"$regex": search_query, "$options": "i"}},  # Search by entity name
                {"entities.type": {"$regex": search_query, "$options": "i"}}  # Search by type
            ]
        }},
        {"$group": {
            "_id": {"entity": "$entities.entity", "type": "$entities.type"},  # Group by both 'entity' and 'type'
            "count": {"$sum": 1}  # Count occurrences
        }},
        {"$sort": {"count": -1}},  # Sort by count, descending
        {"$limit": 50}  # Limit the results to the top 50 to avoid performance issues
    ]

    # Run the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Build response in JSON format
    response = [{
        "entity": row['_id']['entity'],
        "type": row['_id']['type'],
        "count": row['count']
    } for row in result]

    # Return the result as JSON
    return jsonify(response), 200

#24
@app.route('/top_entities', methods=['GET'])
def get_top_entities():
    # MongoDB Aggregation pipeline to get top 5 entities by type
    pipeline = [
        {"$unwind": "$entities"},  # Unwind the 'entities' array
        {"$group": {
            "_id": {"entity": "$entities.entity", "type": "$entities.type"},  # Group by both 'entity' and 'type'
            "count": {"$sum": 1}  # Count occurrences
        }},
        {"$sort": {"count": -1}},  # Sort by count, descending
        {"$group": {
            "_id": "$_id.type",  # Group by 'type' (LOC, ORG, etc.)
            "top_entities": {
                "$push": {
                    "name": "$_id.entity",  # Store entity name
                    "value": "$count"  # Store count as value
                }
            }
        }},
        {"$project": {
            "_id": 1,
            "top_entities": {"$slice": ["$top_entities", 5]}  # Get only the top 5 entities for each type
        }}
    ]

    result = list(collection.aggregate(pipeline))

    # Reformat data to match amCharts hierarchy structure
    bubble_data = []
    for item in result:
        children = [{"name": entity['name'], "value": entity['value']} for entity in item['top_entities']]
        bubble_data.append({
            "name": item["_id"],  # The type (LOC, ORG, etc.)
            "children": children  # Top entities as children
        })

    return jsonify(bubble_data), 200

# 25
@app.route('/top_classes', methods=['GET'])
def get_top_classes():
    # MongoDB aggregation pipeline
    pipeline = [
        {"$unwind": "$classes"},  # Unwind the classes array
        {"$match": {"classes.value": {"$ne": None}}},  # Filter out None values
        {"$group": {
            "_id": "$classes.value",  # Group by the value in the classes array
            "count": {"$sum": 1}  # Count the number of occurrences
        }},
        {"$sort": {"count": -1}},  # Sort by count in descending order
        {"$limit": 5}  # Limit to top 5 classes
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Prepare data in a format for amCharts
    chart_data = [{"category": item['_id'], "value": item['count']} for item in result]

    return jsonify(chart_data)



import pytz


@app.route('/articles_last_<int:x>_hours', methods=['GET'])
def articles_last_x_hours(x):
    # Calculate the datetime X hours ago
    utc_now = datetime.now(pytz.utc)
    x_hours_ago = utc_now - timedelta(hours=x)

    # Query to find articles published in the last X hours
    query = {
        "published_time": {"$gte": x_hours_ago.isoformat()}
    }
    articles = collection.find(query)

    # Extract titles and count the articles
    titles = [article["title"] for article in articles]
    count = len(titles)

    # Return a response with both the titles and the count
    if count == 0:
        return jsonify({"message": f"No articles published in the last {x} hours found", "count": 0}), 404

    return jsonify({
        "titles": titles,  # List of article titles
        "count": count  # Number of articles
    })


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


if __name__ == '__main__':
    app.run(debug=True)
