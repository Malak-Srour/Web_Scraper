from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]

# Find distinct entity types
distinct_types = collection.distinct("entities.type")

# Print the distinct entity types
print("Distinct entity types in the collection:", distinct_types)