from ultralytics import YOLO

#Тестирование модели, поддерживает фото/видео
def main():
    path = input("Введите путь к фото/видеофайлу: ")
    model = YOLO('model.pt')
    model.predict(
        source=path,
        save=True, #Сохранять результат
        conf=0.4,
        iou=0.4,
        max_det=5, #Максимальное кол-во объектов на экране
        visualize=False #Визуализация в консоли
    )


if __name__ == "__main__":
    main()