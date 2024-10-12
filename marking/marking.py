import cv2
import json
import os

rect_start = None
rect_end = None
drawing = False

def mouse_callback(event, x, y, flags, param):
    global rect_start, rect_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        rect_start = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            rect_end = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rect_end = (x, y)

def process_photo(path):
    result = dict()
    for file in os.listdir(path):
        file_path = f'{path}/{file}'
        print(file_path)
        if not file_path:
            print("Изображение не выбрано.")
            return

        image = cv2.imread(file_path)
        if image is None:
            print("Не удалось загрузить изображение.")
            return

        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", mouse_callback)

        while True:
            img_copy = image.copy()

            if rect_start and rect_end:
                cv2.rectangle(img_copy, rect_start, rect_end, (0, 255, 0), 2)

            cv2.imshow("Image", img_copy)

            # key = cv2.waitKey(1) & 0xFF
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break


        cv2.destroyAllWindows()

        if rect_start and rect_end:
            result.update({
                file_path: [
                    {"x1": rect_start[0], "y1": rect_start[1]},
                    {"x2": rect_end[0], "y2": rect_end[1]}
                ]
            })

        else:
            result.update({
                file_path: [
                    {"x1": 0, "y1": 0},
                    {"x2": 0, "y2": 0}
                ]
            })
            print("Прямоугольник не был выделен.")
    
    with open('output.csv', 'w') as f:
            json.dump(result, f)
            print(f"Координаты сохранены в output.csv: {result}")

def process_video(path: list, frames: int):
    global frame_coords, rect_start, rect_end

    video_path = path
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Не удалось открыть видео.")
        return
    
    dir_name = path[:-4]
    print(dir_name)
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        pass

    frame_num = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Конец видео.")
            break
        if frame_num % frames == 0:
            cv2.imwrite(f"{dir_name}/frame{frame_num}.jpg", frame)
        frame_num += 1
    
    cap.release()
    
    process_photo(dir_name)

            


def main():
    action = int(input('1. Видео\n2. Фото\n'))
    if action == 1:
        path = input("Введите путь к видеофайлу: ")
        frames = int(input('Введите кол-во кадоров в секунду: '))
        process_video(path, frames)
    elif action == 2:
        path = input("Введите путь к папке изображениями: ")
        process_photo(path)
    

if __name__ == "__main__":
    main()