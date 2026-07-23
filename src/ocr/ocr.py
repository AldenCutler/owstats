import easyocr


class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=True)
        
    def process_image(self, image):
        '''
        Processes the image using OCR and returns the extracted text.
        '''
        result = self.reader.readtext(image)
        extracted_text = " ".join([text[1] for text in result])
        return extracted_text