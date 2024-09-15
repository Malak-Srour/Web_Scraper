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
    """Counts the articles in all JSON files within the specified directory and returns the total count."""
    file_names = sorted([f for f in os.listdir(directory) if f.startswith('articles_202') and f.endswith('.json')])
    total_articles = 0  # Initialize total count
    article_counts = {}
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        article_count = count_articles_in_file(file_path)
        article_counts[file_name] = article_count
        total_articles += article_count  # Add count from each file to total
        print(f"Total articles in {file_name}: {article_count}")
    print(f"\nGrand total of articles across all files: {total_articles}")  # Print total count of all articles
    return article_counts, total_articles

# Specify the directory where the JSON files are stored
directory = 'articles'
article_counts, grand_total = count_articles_in_directory(directory)
