import cv2
import numpy as np
from ultralytics import YOLO


def main():
    # 加载预训练的YOLOv8实例分割模型
    model = YOLO('/home/ubuntu/yolov8/runs/segment/train14/weights/best.pt')  # 使用官方预训练模型或替换为你的自定义模型路径

    # 初始化摄像头（0通常代表默认摄像头）
    cap = cv2.VideoCapture(2)

    while cap.isOpened():
        # 读取摄像头帧
        success, frame = cap.read()
        if not success:
            break

        # 使用YOLOv8进行推理
        results = model(frame, imgsz=640, conf=0.3)  # 调整参数根据需要

        # 处理每个检测结果
        for result in results:
            # 获取掩码和边界框
            masks = result.masks.data.cpu().numpy() if result.masks else []
            boxes = result.boxes.data.cpu().numpy()

            # 绘制掩码
            for mask in masks:
                # 将单通道掩码转换为三通道
                colored_mask = np.zeros_like(frame)
                color = np.random.randint(0, 255, 3).tolist()  # 随机颜色
                colored_mask[mask > 0] = color

                # 叠加掩码（调整alpha值改变透明度）
                frame = cv2.addWeighted(frame, 1, colored_mask, 0.3, 0)

            # 绘制边界框和标签
            for box in boxes:
                x1, y1, x2, y2, conf, cls = box[:6]
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                cls = int(cls)

                # 绘制矩形框
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # 添加标签和置信度
                label = f"{result.names[cls]} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 显示结果
        cv2.imshow('YOLOv8 Instance Segmentation', frame)

        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()