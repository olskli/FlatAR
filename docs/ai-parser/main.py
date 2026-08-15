import os
import glob
from PIL import Image

def preprocess_plan():
    # Находим корень проекта от текущей папки
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    # Ищем любую картинку в test-plans
    search_pattern = os.path.join(project_root, "**", "test-plans", "*.*")
    plans = [f for f in glob.glob(search_pattern, recursive=True) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not plans:
        print("Ошибка: файлы в папке test-plans не найдены.")
        return

    img_path = plans[0]
    print(f"Обрабатываем файл: {img_path}")

    # Переводим в Ч/Б и делаем бинаризацию
    img = Image.open(img_path).convert("L")
    threshold = 200
    bw_img = img.point(lambda p: 255 if p > threshold else 0)

    # Сохраняем рядом со скриптом
    out_path = os.path.join(current_dir, "processed_plan.png")
    bw_img.save(out_path)
    print(f"Успешно сохранено в: {out_path}")

if __name__ == "__main__":
    preprocess_plan()
