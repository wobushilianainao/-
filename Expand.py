import cv2
import numpy as np
import os
import random
from PIL import Image

def horizontal_flip(image, labels):
    """水平翻转"""
    flipped_img = cv2.flip(image, 1)
    new_labels = []
    for label in labels:
        class_id, x, y, w, h = label
        new_x = 1.0 - x
        new_labels.append([class_id, new_x, y, w, h])
    return flipped_img, new_labels


def vertical_flip(image, labels):
    """垂直翻转"""
    flipped_img = cv2.flip(image, 0)
    new_labels = []
    for label in labels:
        class_id, x, y, w, h = label
        new_y = 1.0 - y
        new_labels.append([class_id, x, new_y, w, h])
    return flipped_img, new_labels


def random_rotate(image, labels, angle_range=(-30, 30)):
    """随机旋转"""
    h, w = image.shape[:2]
    angle = random.uniform(angle_range[0], angle_range[1])

    # 计算旋转矩阵
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # 计算新边界尺寸
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # 调整旋转矩阵
    M[0, 2] += (nW - w) / 2
    M[1, 2] += (nH - h) / 2

    # 执行旋转
    rotated_img = cv2.warpAffine(image, M, (nW, nH), flags=cv2.INTER_LINEAR)

    new_labels = []
    for label in labels:
        class_id, x_center, y_center, bw, bh = label

        # 转换为绝对坐标
        x = x_center * w
        y = y_center * h

        # 创建边界框坐标并旋转
        points = np.array([
            [x - bw * w / 2, y - bh * h / 2],
            [x + bw * w / 2, y - bh * h / 2],
            [x + bw * w / 2, y + bh * h / 2],
            [x - bw * w / 2, y + bh * h / 2]
        ])
        points = np.array([points], dtype=np.float32)
        transformed = cv2.transform(points, M)[0]

        # 计算新的边界框
        x_coords = transformed[:, 0]
        y_coords = transformed[:, 1]

        x_min = max(0, np.min(x_coords) / nW)
        x_max = min(1, np.max(x_coords) / nW)
        y_min = max(0, np.min(y_coords) / nH)
        y_max = min(1, np.max(y_coords) / nH)

        if x_max <= x_min or y_max <= y_min:
            continue  # 过滤无效框

        new_x = (x_min + x_max) / 2
        new_y = (y_min + y_max) / 2
        new_w = x_max - x_min
        new_h = y_max - y_min

        new_labels.append([class_id, new_x, new_y, new_w, new_h])

    return rotated_img, new_labels

def random_translate(image, labels, max_ratio=0.2):
    """随机平移（终极修复+兼容性版本）"""
    # 输入验证
    if not isinstance(image, np.ndarray):
        raise ValueError("Input image must be numpy array")
    h, w = image.shape[:2]
    if h == 0 or w == 0:
        return image, labels

    # 计算平移量（双精度转单精度）
    tx = np.float32(random.uniform(-max_ratio, max_ratio) * w)
    ty = np.float32(random.uniform(-max_ratio, max_ratio) * h)

    # 构建变换矩阵
    M = np.array([[1.0, 0.0, tx],
                  [0.0, 1.0, ty]],
                 dtype=np.float32).reshape(2, 3)

    # OpenCV 4.x+ 版本兼容处理
    if cv2.__version__ >= '4.5':
        M = cv2.UMat(M)

    # 执行仿射变换
    translated_img = cv2.warpAffine(
        image,
        M,
        (int(w), int(h)),  # 确保整数尺寸
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101
    )

    new_labels = []
    for label in labels:
        class_id, x, y, bw, bh = label

        # 计算平移后的坐标
        new_x = (x * w + tx) / w
        new_y = (y * h + ty) / h

        # 边界检查
        x_min = max(0, new_x - bw / 2)
        x_max = min(1, new_x + bw / 2)
        y_min = max(0, new_y - bh / 2)
        y_max = min(1, new_y + bh / 2)

        if x_max <= x_min or y_max <= y_min:
            continue

        new_w = x_max - x_min
        new_h = y_max - y_min
        new_center_x = (x_min + x_max) / 2
        new_center_y = (y_min + y_max) / 2

        new_labels.append([class_id, new_center_x, new_center_y, new_w, new_h])

    return translated_img, new_labels

def validate_image(img):
    """验证图像有效性"""
    return isinstance(img, np.ndarray) and img.dtype == np.uint8 and img.size > 0

def safe_horizontal_flip(image, labels):
    # if not validate_image(image):
    #     return image, labels
    try:
        return horizontal_flip(image, labels)
    except:
        return image, labels

def safe_vertical_flip(image, labels):
    if not validate_image(image):
        return image, labels
    try:
        return vertical_flip(image, labels)
    except:
        return image, labels

def safe_rotate(image, labels):
    # if not validate_image(image):
    #     return image, labels
    try:
        return random_rotate(image, labels)
    except:
        return image, labels

def safe_translate(image, labels):
    # if not validate_image(image):
    #     return image, labels
    try:
        return random_translate(image, labels)
    except:
        return image, labels

def augment_and_save(image_path, label_path, output_dir, augmentations):
    # 读取数据
    image = cv2.imread(image_path)
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)
    if image is None:
        print("图像读取失败！检查路径和文件格式")
    else:
        print(f"图像类型：{type(image)}, 形状：{image.shape}")
    # if not isinstance(image, np.ndarray):
    #     print(f"无法读取图像: {image_path}")
    #     return
        # 初始化增强结果
    aug_image = image.copy()
    aug_labels = []
    with open(label_path, 'r') as f:
        for line in f:
            parts = list(map(float, line.strip().split()))
            if len(parts) == 5:
                aug_labels.append(parts)

    # 安全增强流程
    try:
        for aug in augmentations:
            if random.random() < 0.5:  # 统一概率控制
                if aug == 'hflip':
                    aug_image, aug_labels = safe_horizontal_flip(aug_image, aug_labels)
                elif aug == 'vflip':
                    aug_image, aug_labels = safe_vertical_flip(aug_image, aug_labels)
                elif aug == 'rotate':
                    aug_image, aug_labels = safe_rotate(aug_image, aug_labels)
                elif aug == 'translate':
                    aug_image, aug_labels = safe_translate(aug_image, aug_labels)

                # 增强后立即验证
                if not validate_image(aug_image):
                    raise ValueError("增强后图像无效")
    except Exception as e:
        print(f"增强失败 {image_path}: {str(e)}")
        return
    # 保存结果
    aug_image_array = np.array(aug_image)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_img_path = os.path.join(output_dir, 'images', f'{base_name}_aug.jpg')
    output_label_path = os.path.join(output_dir, 'labels', f'{base_name}_aug.txt')

    os.makedirs(os.path.dirname(output_img_path), exist_ok=True)
    cv2.imwrite(output_img_path, aug_image_array)

    with open(output_label_path, 'w') as f:
        for label in aug_labels:
            f.write(' '.join(map(str, label)) + '\n')


def batch_augmentation(input_dir, output_dir, augmentations, num_aug=5):
    """批量处理数据集"""
    image_dir = os.path.join(input_dir, 'images')
    label_dir = os.path.join(input_dir, 'labels')

    for img_name in os.listdir(image_dir):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            base_name = os.path.splitext(img_name)[0]
            img_path = os.path.join(image_dir, img_name)
            label_path = os.path.join(label_dir, f'{base_name}.txt')

            if not os.path.exists(label_path):
                continue

            for i in range(num_aug):
                augment_and_save(img_path, label_path, output_dir, augmentations)


# 使用示例
if __name__ == "__main__":
    INPUT_DIR = './data'
    OUTPUT_DIR = './data'
    AUGMENTATIONS = ['hflip', 'vflip', 'rotate', 'translate']

    batch_augmentation(INPUT_DIR, OUTPUT_DIR, AUGMENTATIONS, num_aug=3)
