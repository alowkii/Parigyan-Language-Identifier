from PIL import Image
import pytesseract

def extract_text_from_image():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    image_path = 'images/image.png'

    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, lang='ocrb+eng+rus+hin+kor+jap')

    with open('input/input.txt', 'w', encoding='utf-8') as file:
        file.write(text)