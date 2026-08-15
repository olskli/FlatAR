import os
import glob
import cv2
import numpy as np
from PIL import Image

def process_and_find_contours():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    # 1. Ищем файл планировки
    search_pattern = os.path.join(project_root, "**", "test-plans", "*.*")
    plans = [f for f in glob.glob(search_pattern, recursive=True) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not plans:
        print("Ошибка: файлы в папке test-plans не найдены.")
        return

    img_path = plans[0]
    print(f"Обрабатываем файл: {img_path}")

    # 2. Делаем Ч/Б обработку
    img_pil = Image.open(img_path).convert("L")
    bw_img = img_pil.point(lambda p: 255 if p > 200 else 0)
    processed_path = os.path.join(current_dir, "processed_plan.png")
    bw_img.save(processed_path)

    # 3. Находим контуры через OpenCV
    img_cv = cv2.imread(processed_path)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Рисуем зеленые контуры
    result_img = img_cv.copy()
    cv2.drawContours(result_img, contours, -1, (0, 255, 0), 2)

    output_path = os.path.join(current_dir, "contours_plan.png")
    cv2.imwrite(output_path, result_img)
    print(f"Найдено контуров: {len(contours)}. Результат сохранен в: {output_path}")

if __name__ == "__main__":
    process_and_find_contours()
