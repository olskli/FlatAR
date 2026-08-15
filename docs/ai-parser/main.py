import os
from PIL import Image

def load_plan(image_path):
    if not os.path.exists(image_path):
        print(f"Ошибка: файл {image_path} не найден.")
        return None
    
    img = Image.open(image_path)
    print(f"Планировка успешно загружена!")
    print(f"Размер изображения: {img.size[0]}x{img.size[1]} пикселей")
    return img

if __name__ == "__main__":
    # Пробуем открыть первую тестовую планировку
    test_image = "../test-plans/Снимок экрана 2026-08-15 в 10.15.29.png"  # указать имя твоего файла
    load_plan(test_image)
