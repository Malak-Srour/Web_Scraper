import os
import json
from pymongo import MongoClient
import stanza

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]

# Initialize Stanza pipeline for Arabic
nlp = stanza.Pipeline('ar', processors='tokenize,ner')

# Create the 'entities' folder if it doesn't exist
if not os.path.exists('entities'):
    os.makedirs('entities')

# Initialize counter
counter = 0
total_articles = collection.count_documents({})

# Process articles and save recognized entities as JSON files
for article in collection.find():
    full_text = article.get("full_text", "")

    # Perform entity recognition on the full_text
    doc = nlp(full_text)

    # Extract entities from the Stanza doc
    entities = [{"entity": ent.text, "type": ent.type} for ent in doc.ents]

    # Save the recognized entities in a JSON file
    article_id = str(article['_id'])
    file_path = os.path.join('entities', f'{article_id}.json')

    # Create a dictionary with article info and entities
    article_data = {
        "id": article_id,
        "title": article.get("title", ""),
        "full_text": full_text,
        "entities": entities
    }

    # Write the dictionary to a JSON file
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(article_data, json_file, ensure_ascii=False, indent=4)

    # Increment the counter
    counter += 1

    # Print progress message with counter and total articles
    print(f"[{counter}/{total_articles}] Entities for Article ID {article_id} saved to {file_path}.")

print(f"Entity extraction and saving completed. {counter} articles processed.")
