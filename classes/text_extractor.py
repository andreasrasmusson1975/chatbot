from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class TextExtractor:
    def __init__(self,jpg_path):
        self.jpg_path = jpg_path
        self.image = Image.open(jpg_path)
        self.text = self.get_text()
        
    def get_text(self):
        return pytesseract.image_to_string(self.image)


