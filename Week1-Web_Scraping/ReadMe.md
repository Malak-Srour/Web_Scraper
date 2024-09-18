# AlMayadeen Article Analyzer

This project is a comprehensive solution to scrape, analyze, store, and visualize articles from Al Mayadeen's website. The project consists of multiple phases, covering web scraping, data storage in MongoDB, data analysis with NLP techniques, and visualization through amCharts in a Flask-based API.

## Project Components

### Week 1 - Web Scraping Al Mayadeen Articles

#### Objective: 
Scrape articles from Al Mayadeen's sitemap, extract metadata, and save the data in JSON format for analysis.

#### Key Scripts:
- `web_scraper.py`: Main script for scraping articles from Al Mayadeen's sitemap and saving them as JSON files organized by month.
- `nb_of_articles.py`: A utility script to count and display the number of articles stored in each JSON file.

---

### Week 2 - Data Storage and Flask API

#### Objective: 
Store scraped articles in MongoDB and create a Flask API to query and analyze the data.

#### Key Scripts:
- `data_storage.py`: Loads JSON files and inserts the articles into MongoDB.
- `app.py`: Flask API to provide endpoints for querying and analyzing the data stored in MongoDB.

---

### Week 3 - Data Visualization with amCharts

#### Objective: 
Visualize data using amCharts. Implement charts to showcase insights like keyword frequency, top authors, and article publication trends.

#### Key Scripts:
- `templates/`: Contains HTML templates for rendering charts.
- `static/`: Contains the JavaScript and CSS files for charts.
- `app.py`: Serves the data for charts through Flask API endpoints.

#### Sample Charts:

- **Top Authors Chart**:
  ![Top Authors Chart](path_to_image/top_authors_chart.png)

- **Keyword Frequency Word Cloud**:
  ![Keyword Frequency Word Cloud](path_to_image/keyword_wordcloud.png)

- **Articles by Language**:
  ![Articles by Language](path_to_image/articles_by_language_chart.png)

---

### Week 4 - Advanced Data Analysis

#### Objective: 
Perform advanced data analysis using Natural Language Processing (NLP) techniques, such as sentiment analysis and entity recognition.

#### Key Scripts:
- `sentiment_analysis.py`: Runs sentiment analysis on the articles to identify positive, neutral, or negative sentiments.
- `entity_recognition.py`: Extracts named entities (people, places, organizations) from the article text.

---

### Week 5 - Code Refactoring and Optimization

#### Objective: 
Refactor code using SOLID principles and design patterns. Introduce unit tests and optimize MongoDB queries for better performance.

---

## Setup

Follow these steps to get your development environment set up:

### Prerequisites

Ensure Python 3.6+ is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).  
MongoDB: Ensure MongoDB is installed and running locally. Download it from [mongodb.com](https://www.mongodb.com/try/download/community).

---

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://your-repository-link.git
   cd your-project-directory

2. **Install Required Python Libraries**:
   ```bash
    pip install -r Requirements.txt

### Usage:
1. Scraping Articles (Week 1):

    To scrape articles from the website, run
   ```bash
    python web_scraper.py

2. Storing Articles in MongoDB (Week 2):

    After scraping, load the articles into MongoDB:
   ```bash
    python data_storage.py

3. Running the Flask API (Week 2 & Week 3):

    Start the Flask API to serve data and visualizations:
   ```bash
    python app.py
You can access the API and visualizations via:
http://127.0.0.1:5000/

4. Performing Sentiment Analysis (Week 4):

    Run sentiment analysis on the articles:
   ```bash
    python sentiment_analysis.py
   
5. Extracting Entities (Week 4):

    Run entity recognition on the articles:
   ```bash
    python entity_recognition.py
   

6. Visualizing Data (Week 3 & Week 4):

    Navigate to the dashboard to see charts and data visualizations once the Flask API is running.

## API Endpoints

The Flask API provides several endpoints for querying the data and visualizing it through interactive charts:

### Dashboard Routes

- `/dashboard`: Main dashboard to view all data visualizations.
- `/authors_dashboard`: Displays top authors.
- `/keywords_dashboard`: Displays top keywords.
- `/date_time_dashboard`: Displays data and charts by date and time.
- `/word_count_dashboard`: Displays articles by word count.
- `/classes_dashboard`: Displays articles by class.
- `/sentiment_analysis_dashboard`: Displays sentiment analysis charts.

### Data Visualization Routes

- `/top_authors_chart`: Displays a chart of the top authors.
- `/articles_by_word_count_chart`: Displays articles grouped by word count.
- `/articles_by_language_chart`: Displays articles grouped by language.
- `/recent_articles_chart`: Displays the most recent articles.
- `/articles_with_video_chart`: Displays articles with and without video.
- `/longest_articles_chart`: Displays the longest articles by word count.
- `/shortest_articles_chart`: Displays the shortest articles (excluding zero word count).
- `/articles_by_keyword_count_chart`: Displays articles by the number of keywords.
- `/articles_by_thumbnail_chart`: Displays articles with or without thumbnails.
- `/articles_updated_chart`: Displays articles updated after publication.
- `/popular_keywords_chart`: Displays the most popular keywords in the last X days.
- `/articles_by_month`: Displays articles by published month.
- `/articles_by_word_count_range`: Displays articles by word count range.
- `/articles_with_more_than`: Displays articles with more than N words.
- `/articles_by_title_length_chart`: Displays articles grouped by title length.
- `/articles_by_date_chart`: Displays articles grouped by publication date.
- `/articles_by_sentiment_chart`: Displays articles grouped by sentiment (positive, neutral, negative).
- `/most_positive_articles_chart`: Displays the most positive articles.
- `/most_negative_articles_chart`: Displays the most negative articles.
- `/author_articles_chart`: Displays articles written by a specific author.
- `/articles_by_keyword_chart`: Displays articles grouped by specific keywords.
- `/entites_chart`: Displays entities extracted from articles.
- `/top_entites_chart`: Displays top entities in a force-directed bubble chart.
- `/top_classes_chart`: Displays the top classes found in articles.
- `/last_x_hours_chart`: Displays articles published in the last X hours.


## Tools and Libraries

- **Python**: The primary programming language used in this project.
- **Flask**: A web framework for building the API to serve and visualize data.
- **MongoDB**: The database used to store the scraped article data.
- **TextBlob**: Used for performing sentiment analysis on the articles.
- **Stanza**: Used for named entity recognition (NER) to extract entities like people, places, and organizations from the articles.
- **amCharts**: A JavaScript library used for creating interactive charts to visualize the data.
- **BeautifulSoup & Requests**: For web scraping the Al Mayadeen website.

