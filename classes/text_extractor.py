"""
This module provides the text extractor class for extracting text from an image. Extraction
is performed using tesseract which requires third party installation.
"""

# Perform necessary imports
from PIL import Image
import pytesseract
from pathlib import Path

# Explicitly set the path to tesseract.exe. This is not required if the user has re-
# booted after installation of tesseract but better safe than sorry.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextExtractor:
    """
    This class implements functionality for extracting text from an image using tesseract.
    
    Attributes:
        jpg_path (Path): A path to a jpg image
        image (Image): A PIL Image object
        text (str): The text extracted from the image

    """
    def __init__(self,jpg_path: Path):
        # Store the image path, load the image and extract the text
        self.jpg_path = jpg_path
        self.image = Image.open(jpg_path)
        self.text = self.get_text()
        
    def get_text(self) -> str:
        # Extract the text from the image.
        return pytesseract.image_to_string(self.image)


