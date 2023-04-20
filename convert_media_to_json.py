import json
import os
import subprocess
from datetime import datetime

import pymongo
from colorama import Fore, Style
from PIL import Image
from pytesseract import *

# Install required packages
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

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
        newArray.append({'name': content, 'status': False})
    
    # Check if the file is an txt file.
    if file.endswith('.txt'):
        # Read the content of the source file
        with open(file_path, 'r') as source_file:
            # Read the contents of the file and split it into lines
            lines = source_file.read().splitlines()
            for line in lines:
                # Append the object to the array
                newArray.append({'name': line, 'status': False})

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
        print(f"{Fore.GREEN} {len(unique_objects)} New documents inserted successfully. {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Value exists in at least one document, not inserting.{Style.RESET_ALL}")
   
