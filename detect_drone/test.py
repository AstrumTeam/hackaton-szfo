import os
from ultralytics import YOLO
import shutil

def process_videos(input_folder, model_path, conf=0.35, iou=0.4):
    if not os.path.exists(input_folder):
        print(f"Папка {input_folder} не существует!")
        return
    
    model = YOLO(model_path)

    for video_file in os.listdir(input_folder):
        if video_file.endswith(('.mp4', '.avi', '.mov')):
            input_path = os.path.join(input_folder, video_file)

            results = model.predict(
                source=input_path,
                save=True,
                conf=conf,
                iou=iou,
                max_det=1
            )

            detect_folder = os.path.join('runs', 'detect')
            if os.path.exists(detect_folder):
                latest_result_folder = max([os.path.join(detect_folder, d) for d in os.listdir(detect_folder)], key=os.path.getmtime)

                for result_file in os.listdir(latest_result_folder):
                    if result_file.endswith(('.mp4', '.avi', '.mov')):
                        result_path = os.path.join(latest_result_folder, result_file)
                        output_video_path = os.path.join(input_folder, f'processed_{video_file}')

                        shutil.move(result_path, output_video_path)
                        print(f"Видео {video_file} успешно обработано. Результат сохранен как {output_video_path}")

            if os.path.exists(latest_result_folder) and not os.listdir(latest_result_folder):
                os.rmdir(latest_result_folder)

    print("Обработка всех видео завершена.")

input_folder = input('Введите путь к папке с видео: ')
model_path = 'model-drone.pt'

process_videos(input_folder, model_path)