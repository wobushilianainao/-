from ultralytics import YOLO

# 加载一个模型
model = YOLO('yolov8n-seg.pt')  # 预训练的 YOLOv8n 模型

# 对一系列图像执行批量推理
results = model(['im1.jpg'])  # 返回一个结果对象列表

# 处理结果列表
for result in results:
    boxes = result.boxes  # Boxes 对象，用于边界框输出
    masks = result.masks  # Masks 对象，用于分割掩码输出
    keypoints = result.keypoints  # Keypoints 对象，用于姿态输出
    probs = result.probs  # Probs 对象，用于分类输出

print("boxes输出示意：\n", boxes)
print("masks输出示意：\n", masks)
print("keypoints输出示意：\n", keypoints)
print("probs输出示意：\n", probs)