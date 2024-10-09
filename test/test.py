from ultralytics import YOLO

model = YOLO('test/my-yolo8n-drone.pt')

results = model.predict(
    source='IMG_8209.MP4',
    save=True,
    conf=0.1,
    iou=0.6
)