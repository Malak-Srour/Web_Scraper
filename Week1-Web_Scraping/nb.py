import json
import os

def count_articles_in_file(file_path):
    """Counts the number of articles in a given JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
            return len(articles)
    except FileNotFoundError:
        return "File not found."

def count_articles_in_directory(directory):
    """Counts the articles in all JSON files within the specified directory."""
    file_names = sorted([f for f in os.listdir(directory) if f.startswith('articles_2024') and f.endswith('.json')])
    article_counts = {}
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        article_count = count_articles_in_file(file_path)
        article_counts[file_name] = article_count
        print(f"Total articles in {file_name}: {article_count}")
    return article_counts

# Specify the directory where the JSON files are stored
directory = 'articles'
article_counts = count_articles_in_directory(directory)
