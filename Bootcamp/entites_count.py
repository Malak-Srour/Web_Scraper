import os

# Specify the directory where your JSON files are saved
directory = "entities"

# Get a list of all files in the directory
files_in_directory = os.listdir(directory)

# Filter the list to only include files with the .json extension
json_files = [file for file in files_in_directory if file.endswith(".json")]

# Count the number of JSON files
json_file_count = len(json_files)

# Print the count
print(f"There are {json_file_count} JSON files in the '{directory}' folder.")
