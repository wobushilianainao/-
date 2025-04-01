from ultralytics import YOLO

model = YOLO("/home/ubuntu/yolov8/runs/segment/train14/weights/last.pt")
result = model.train(resume=True)