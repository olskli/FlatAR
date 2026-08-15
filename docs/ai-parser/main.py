import os
import glob
import cv2
import numpy as np
from PIL import Image

def filter_rooms_and_walls():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    search_pattern = os.path.join(project_root, "**", "test-plans", "*.*")
    plans = [f for f in glob.glob(search_pattern, recursive=True) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not plans:
        print("Ошибка: файлы в папке test-plans не найдены.")
        return

    img_path = plans[0]
    img_cv = cv2.imread(img_path)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Бинаризация для получения чистых бинарных масок
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Иерархический поиск контуров (позволяет находить внутренние области — комнаты)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    result_img = img_cv.copy()
    valid_rooms = 0

    # Минимальная площадь контура, чтобы отсечь шум, цифры и текст
    min_area = 1000

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > min_area:
            valid_rooms += 1
            # Аппроксимация контура до прямоугольников/простых полигонов
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            # Рисуем контуры комнат зелёным цветом
            cv2.drawContours(result_img, [approx], -1, (0, 255, 0), 3)

    output_path = os.path.join(current_dir, "filtered_rooms.png")
    cv2.imwrite(output_path, result_img)
    print(f"Отфильтровано: осталось {valid_rooms} крупных объектов/комнат. Результат сохранен в: {output_path}")

if __name__ == "__main__":
    filter_rooms_and_walls()
