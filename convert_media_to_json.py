import json
import os

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

# Check if the output folder exists
while not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# Loop through the files in input folder content
newArray = []
for file in inputContent:
    file_path = os.path.join(inputFolder, file)

    # Check if the file is an image file
    if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
        # Use PyTesseract to convert the text in the image to a txt file
        
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

        # Save the text to a new txt file with the same name as the image file
        txt_path = os.path.join(outputFolder, os.path.splitext(file)[0] + '_output.txt') 
        with open(txt_path, 'w') as f:
            newArray.append({'name': text.split('\n')[0], 'status': False})
            f.write(text.split('\n')[0] + ' updated')

    
    # Check if the file is an txt file.
    if file.endswith('.txt'):
        # Save the text to a new txt file with the same name as the image file
        txt_path = os.path.join(outputFolder, os.path.splitext(file)[0] + '_output.txt')
        with open(file_path, 'r') as source_file:
            # Read the content of the source file
            content = source_file.read()
            newArray.append({'name': content, 'status': False})
            with open(txt_path, 'w') as f:
                f.write(content + ' Updated')



# Check if the file exists
file_path = os.path.join(outputFolder, 'data.json')
while not os.path.exists(file_path):
    with open(file_path, "w") as f:
        json.dump(newArray, f)

# Load existing data from JSON file
# with open(file_path, 'r') as file:
#     data = json.load(file)

# # Append new data to Python object
# data.append(newArray)

# # Write updated object to JSON file
# with open(file_path, 'w') as file:
#     json.dump(data, file)



# Display the successful meesage
print("Finished converting successfully!")
