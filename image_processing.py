import cv2
import pytesseract
import numpy as np
import re

def preprocess_image(image_path):
    """Обрабатывает изображение для лучшего распознавания текста."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_path):
    """Извлекает текст из изображения с помощью OCR."""
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image, lang='rus')
    return text

def parse_wood_data(text):
    """Извлекает ключевые параметры (порода, длина, диаметр, количество, объем) из распознанного текста."""
    wood_entries = []
    lines = text.split('\n')
    
    for line in lines:
        match = re.search(r"(\w+)\s+(\d+)м\s+(\d+)см\s+(\d+)шт\s+(\d+\.\d+)м3", line)
        if match:
            wood_type = match.group(1)
            length = int(match.group(2))
            diameter = int(match.group(3))
            quantity = int(match.group(4))
            volume = float(match.group(5))
            wood_entries.append({
                "wood_type": wood_type,
                "length_cm": length,
                "diameter_cm": diameter,
                "quantity": quantity,
                "volume_m3": volume
            })
    
    return wood_entries

# Пример использования
if __name__ == "__main__":
    image_path = "example.jpg"  # Здесь должен быть путь к загруженному изображению
    extracted_text = extract_text(image_path)
    parsed_data = parse_wood_data(extracted_text)
    print(parsed_data)
