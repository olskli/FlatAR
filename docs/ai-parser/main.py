import os
import glob
import cv2
import numpy as np
from PIL import Image

def find_contours():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    processed_path = os.path.join(current_dir, "processed_plan.png")

    if not os.path.exists(processed_path):
        print("Ошибка: файл processed_plan.png не найден. Сначала запустите предобработку.")
        return

    # Загружаем обработанное изображение в OpenCV
    img = cv2.imread(processed_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Инвертируем: стены должны быть белыми (255), а фон черным (0) для поиска контуров
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Находим контуры
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Отрисовываем найденные контуры зелёным цветом
    result_img = img.copy()
    cv2.drawContours(result_img, contours, -1, (0, 255, 0), 2)

    output_path = os.path.join(current_dir, "contours_plan.png")
    cv2.imwrite(output_path, result_img)
    print(f"Найдено контуров: {len(contours)}. Результат сохранен в: {output_path}")

if __name__ == "__main__":
    find_contours()
