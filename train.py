# from ultralytics import YOLO
#
#
# # 加载模型
# model = YOLO('yolov12n.yaml').load('yolov12n.pt')  # 从YAML构建并转移权重
#
# if __name__ == '__main__':
#     # 训练模型
#     results = model.train(data='cube.yaml', epochs=10, imgsz=512)
#
#     metrics = model.val()
# from ultralytics import YOLO
#
# model = YOLO('yolo11n.pt')  # 加载预训练模型
#
# results = model.train(
#     data='cube.yaml',
#     epochs=100,
#     imgsz=640,
#     batch=16,
#     device=0,  # 使用GPU 0
#     optimizer='SGD',
#     lr0=0.001
# )
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(r'ultralytics/cfg/models/11/yolo11-seg.yaml')

    model.train(data=r'cube.yaml',
                imgsz=640,
                epochs=100,
                single_cls=True,
                batch=16,
                workers=10,
                device='0',
                )


