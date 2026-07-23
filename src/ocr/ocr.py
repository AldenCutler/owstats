import easyocr
import cv2
import pytesseract
from PIL import Image, ImageChops
import numpy as np

PYTESSERACT_CONFIG = (
    "--psm 7 "
    "--oem 3 "
    "-c tessedit_char_whitelist=0123456789,"
)

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=True)
        
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        '''
        Preprocess the image for better OCR results.
        '''
        # get the bounding box of the non-white content
        bbox = image.getbbox()
        image = image.crop(bbox)
        
        # Convert to grayscale
        gray_image = image.convert("L")
        np_image = np.array(gray_image)
        
        # Apply thresholding to get a binary image
        # _, thresh_image = cv2.threshold(np_image, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Enlarge the image to improve OCR accuracy
        thresh_image = cv2.resize(np_image, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        processed_image = Image.fromarray(thresh_image)
        
        return processed_image
    
    def white_color_mask(self, image: Image.Image) -> Image.Image:
        r, g, b = image.copy().convert("RGB").split()
        
        r_mask = r.point(lambda i: 255 if i > 245 else 0)
        g_mask = g.point(lambda i: 255 if i > 245 else 0)
        b_mask = b.point(lambda i: 255 if i > 245 else 0)
        # r_mask = r.point(lambda i: 255 if i == 255 else 0)
        # g_mask = g.point(lambda i: 255 if i == 255 else 0)
        # b_mask = b.point(lambda i: 255 if i == 255 else 0)

        white_mask = ImageChops.logical_and(r_mask.convert("1"), g_mask.convert("1"))
        white_mask = ImageChops.logical_and(white_mask, b_mask.convert("1"))

        return white_mask.convert("RGB")
        
    def extract_text_from_sections(self, sections: dict[str, Image.Image]) -> dict:
        '''
        Processes the image using OCR and returns the extracted text.
        '''
        extracted_texts = {}
        for key, image in sections.items():
            if "hero" not in key.lower():
                image = self.preprocess_image(image)
                image = self.white_color_mask(image)
                # image.save(f"screenshots/preprocessed/{key}.png")
            
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            extracted_text = pytesseract.image_to_string(np.array(image), config=PYTESSERACT_CONFIG)
            
            if not extracted_text.strip():
                # No text detected in the image. Try easyocr as a fallback.
                result = self.reader.readtext(np.asarray(image))
                extracted_text = " ".join([text[1] for text in result])
            
            extracted_text = extracted_text.replace("\n", " ").replace("\r", " ").replace(",", "").strip()
            extracted_texts[key] = extracted_text.lower().strip()

        return extracted_texts