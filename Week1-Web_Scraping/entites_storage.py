import os
import json
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to handle MongoDB _id

# Step 1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['almayadeen']
collection = db['articles']

# Step 2: Path to the folder containing JSON files (Fixed the path issue using raw string)
folder_path = r'/Week1-Web_Scraping/entities'

updated_count = 0

# Step 3: Loop through each JSON file and update the corresponding article in MongoDB
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            article_data = json.load(file)
            article_postid = article_data.get('id')  # Assuming the JSON file has an 'id' field that matches 'postid'

            # Convert article_postid to ObjectId if needed
            try:
                article_postid = ObjectId(article_postid)  # Convert to ObjectId if possible
            except:
                pass  # If it's already a string, we don't convert it

            # Step 4: Prepare the entities array to be inserted
            entities = article_data.get('entities', [])

            # Step 5: Update the document in MongoDB by matching 'postid' field and adding the 'entities' field
            result = collection.update_one(
                {'_id': article_postid},  # Match the document by '_id' field
                {'$set': {'entities': entities}}  # Update or insert the 'entities' field
            )

            # Print the result of the update and increment the counter
            if result.modified_count > 0:
                updated_count += 1
                print(f'{updated_count} Updated document with postid: {article_postid}')
            else:
                print(f'No document found or updated for postid: {article_postid}')

# Step 6: Print the total number of updated documents
print(f"Entities field updated for all applicable articles. Total documents updated: {updated_count}")
