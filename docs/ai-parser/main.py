import os
from PIL import Image, ImageFilter, ImageOps

def preprocess_plan(image_path, output_path="processed_plan.png"):
    if not os.path.exists(image_path):
        print(f"Ошибка: файл {image_path} не найден.")
        return None
    
    # Открываем изображение
    img = Image.open(image_path)
    
    # Переводим в оттенки серого
    gray_img = img.convert("L")
    
    # Увеличиваем контрастность и делаем бинаризацию (только черные стены и белый фон)
    threshold = 200
    bw_img = gray_img.point(lambda p: 255 if p > threshold else 0)
    
    # Сохраняем обработанный результат
    bw_img.save(output_path)
    print(f"Планировка обработана и сохранена в: {output_path}")
    return bw_img

if __name__ == "__main__":
    test_image = "../../test-plans/Снимок экрана 2026-08-15 в 10.20.51" # укажи имя своего файла
    preprocess_plan(test_image)
