## Media Data to JSON Converter

This Python script takes a folder with image and text files and creates a JSON file that can be imported into a MongoDB database. Each file is read, and the content of the files is converted into an object that is added to an array of objects. The resulting array of objects is saved to a JSON file and checked against existing data in a MongoDB database.
Getting Started

To run this script, you will need to install several packages specified in the requirements.txt file. You can install these packages by running the following command:

    pip install -r requirements.txt

Prerequisites

This script requires Python 3.6 or higher and the following packages:

    pymongo
    colorama
    pillow
    pytesseract

Installing

After installing the required packages, you can run the script using the following command:

    python image_text_to_mongo.py

Note

    For Windows users, additional installation may be required for Tesseract OCR. Please refer to the Tesseract OCR GitHub repository for more information.

How it Works

    1- The script checks for the required packages and installs them if they are not already installed.
    2- The folder paths for input, output, and log files are set.
    3- The script reads each file in the input folder and checks if it is an image or text file.
    4- If it is an image file, the script uses the PyTesseract library to extract  the text from the image and create an object with the text as the name and a status of False.
    5- If it is a text file, the script reads the contents of the file and creates an object for each line with the line as the name and a status of False.
    6- The script saves the file path and date-time in a log file.
    7- The script creates a JSON file and saves the array of objects to it.
    8- The script checks the JSON file against an existing MongoDB database to see if any new documents can be inserted.
    9- The script connects to the MongoDB database and retrieves all the documents in the collection.
    10- The script compares the names of the new objects to the names in the existing documents and creates a list of unique objects.
    11- The script inserts the unique objects into the collection and prints a success message.

Authors

    Oussama Bensaid - OSBensaid

License

This project is licensed under the MIT License
