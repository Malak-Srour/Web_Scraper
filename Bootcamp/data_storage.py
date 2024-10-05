import pymongo
import json
import os

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit()

db = client["almayadeen"]
collection = db["articles"]

# Directory containing your JSON files
directory = 'articles'

# Loop through each JSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)
            # Insert data into MongoDB
            collection.insert_many(data)
            print(f"Data from {filename} inserted successfully!")

print("All data inserted successfully!")
