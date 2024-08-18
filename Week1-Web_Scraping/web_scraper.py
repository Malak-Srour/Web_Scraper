import requests
from bs4 import BeautifulSoup
import json
import os

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
    script_tag = soup.find('script', {'type': 'text/tawsiyat'})
    if script_tag:
        return json.loads(script_tag.text)
    return None

def save_articles_data(all_data, directory='articles', file_name='articles_2023_08.json'): #change file name here
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print(f"All articles saved to {file_path}")

# Main Function
#change url here
sitemap_url = 'https://www.almayadeen.net/sitemaps/all/sitemap-2023-8.xml'
sitemap_content = fetch_sitemap(sitemap_url)
url_count = count_urls_in_sitemap_length(sitemap_content)

print(f"Total URLs found: {url_count}")
urls = extract_urls_from_sitemap(sitemap_content)

#change nb of artivle here
urls = urls[:300]

all_articles = []
for url in urls:
    article_data = fetch_and_parse_article(url)
    if article_data:
        all_articles.append(article_data)
        print(f"Article from {url} added to {os.path.join('articles', 'articles_2023_08.json')}") #change file name here
    else:
        print(f"No data found for {url}")

save_articles_data(all_articles)

print(f"Total number of articles written to the JSON file: {len(all_articles)}")
