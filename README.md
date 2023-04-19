Media Data to JSON Converter

This Python script converts media data (image and text) into JSON format. It uses the Tesseract OCR engine to extract text from images.
Installation

Before running the script, you need to install the required dependencies:

    pytesseract
    pillow

You can install them using pip by running the following command in the terminal:

pip install pytesseract pillow

Usage

    Place the media files you want to convert in the "inputs" folder.
    Run the script "convert_media_to_json.py" in the command line.
    The converted JSON files will be stored in the "output" folder.

The script checks if the media file is an image or a text file. If it is an image file, it extracts the text using the Tesseract OCR engine and saves it to a JSON file with the same name as the image file. If it is a text file, it simply saves the content to a JSON file with the same name as the text file.
Example

Here is an example of how to run the script:

python convert_media_to_json.py

Requirements

    Python 3.x
    Tesseract OCR engine
    pytesseract
    pillow

License

This project is licensed under the MIT License.
