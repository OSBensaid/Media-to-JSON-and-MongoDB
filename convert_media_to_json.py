import json
import os
from datetime import datetime

import pymongo
from PIL import Image
from pytesseract import *

# Additional installation for windows user
# https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Change the directory & Get the current working 
# os.chdir('./scripts')
mainFolder = os.getcwd()

# Set the paths for the folders
inputFolder = os.path.join(mainFolder, 'inputs')
inputContent = os.listdir(inputFolder)
outputFolder = os.path.join(mainFolder, 'output')
log_path = os.path.join(outputFolder,  '_log.txt') 

# Check if the output folder exists
while not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    # Create new file
    open(log_path, "w")

# Loop through the files in input folder content
newArray = []
for file in inputContent:
    file_path = os.path.join(inputFolder, file)
    
    # Check if the file is an image file
    if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
        # Use PyTesseract to convert the text in the image to a txt file
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        content = text.split('\n')[0]
    
    # Check if the file is an txt file.
    if file.endswith('.txt'):
        # Read the content of the source file
        with open(file_path, 'r') as source_file:
            content = source_file.read()
    
    newArray.append({'name': content, 'status': False})

    # Save the file path and date-time in log file
    with open(log_path, 'a') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + file_path + '\n')

# Check if the file exists
file_path = os.path.join(outputFolder, 'data.json')
while not os.path.exists(file_path):
    with open(file_path, "w") as f:
        json.dump(newArray, f)

# Load existing data from JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["school"]
    collection = db["students"]

    # retrieve all documents in the collection
    original_names = [item['name'] for item in collection.find({}, {"_id": 0})]
    unique_objects = [item for item in newArray if item['name'] not in original_names]
    
    # insert all the documents if the value does not exist in any document
    if unique_objects:
        # Insert the list of documents into the collection
        collection.insert_many(unique_objects)
        length_of_list = len(unique_objects)
        print(length_of_list , 'New documents inserted successfully.')
    else:
        print('Value exists in at least one document, not inserting.')
        
# Display the successful meesage
print("Completed successfully!")
