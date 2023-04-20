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
    # Create a MongoClient instance
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Create a database instance
    db = client["school"]

    # Create a collection instance
    collection = db["students"]

    # Insert the list of documents into the collection
    result = collection.insert_many(data)

# # Append new data to Python object
# data.append(newArray)

# # Write updated object to JSON file
# with open(file_path, 'w') as file:
#     json.dump(data, file)

# Display the successful meesage
print("Completed successfully!")
