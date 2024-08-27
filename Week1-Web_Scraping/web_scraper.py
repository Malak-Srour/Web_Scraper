import requests
from bs4 import BeautifulSoup
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Article:
    url: str
    type: str
    postid: str
    title: str
    thumbnail: str
    video_duration: str
    word_count: int
    lang: str
    published_time: str
    last_updated: str
    author: str
    description: str
    full_text: str
    keywords: List[str] = field(default_factory=list)
    classes: List[Dict[str, str]] = field(default_factory=list)


def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_urls_from_sitemap(content):
    soup = BeautifulSoup(content, 'xml')
    urls = [url.loc.text for url in soup.find_all('url')]
    return urls


def count_urls_in_sitemap_length(content):
    soup = BeautifulSoup(content, 'xml')
    urls = soup.find_all('url')
    return len(urls)


def fetch_and_parse_article(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting script data
    script_tag = soup.find('script', {'type': 'text/tawsiyat'})
    if script_tag:
        data = json.loads(script_tag.text)
        full_text = ' '.join([p.text for p in soup.find_all('p')])

        # Extracting keywords and classes
        keywords = data.get('keywords', '').split(',')
        classes = data.get('classes', [])

        # Creating an Article instance
        article = Article(
            type=data.get('type', ''),
            postid=data.get('postid', ''),
            title=data.get('title', ''),
            url=data.get('url', ''),
            keywords=keywords,
            thumbnail=data.get('thumbnail', ''),
            video_duration=data.get('video_duration', ''),
            word_count=int(data.get('word_count', 0)),
            lang=data.get('lang', ''),
            published_time=data.get('published_time', ''),
            last_updated=data.get('last_updated', ''),
            description=data.get('description', ''),
            author=data.get('author', ''),
            full_text=full_text,
            classes=classes
        )
        return article
    return None


def save_articles_data(all_articles, directory='articles', file_name='articles_2024_1.json'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        articles_data = [article.__dict__ for article in all_articles]
        json.dump(articles_data, f, ensure_ascii=False, indent=4)
    print(f"All articles saved to {file_path}")


# Main Function
sitemap_url = 'https://www.almayadeen.net/sitemaps/all/sitemap-2024-1.xml'  # change URL for each month
file_name = 'articles_2024_1.json'  # change file name
number_of_articles = 500  # number of articles

# Fetch sitemap and article URLs
sitemap_content = fetch_sitemap(sitemap_url)
url_count = count_urls_in_sitemap_length(sitemap_content)
print(f"Total URLs found: {url_count}")

urls = extract_urls_from_sitemap(sitemap_content)
urls = urls[:number_of_articles]

# Process each URL and fetch articles
all_articles = []

article_count = 0

for url in urls:
    article = fetch_and_parse_article(url)
    if article:
        all_articles.append(article)
        article_count += 1
        print(f"Article {article_count} from {url} added to {os.path.join('articles', file_name)}")
    else:
        print(f"No data found for {url}")

# Save all articles to JSON
save_articles_data(all_articles, directory='articles', file_name=file_name)
print(f"Total number of articles written to the JSON file: {len(all_articles)}")
