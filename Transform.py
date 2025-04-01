import json
import os

def labelme2yolo_seg(class_name, json_dir, labels_dir):
    """
        此函数用来将labelme软件标注好的json格式转换为yolov_seg中使用的txt格式
        :param json_dir: labelme标注好的*.json文件所在文件夹
        :param labels_dir: 转换好后的*.txt保存文件夹
        :param class_name: 数据集中的类别标签
        :return:
    """
    list_labels = []  # 存放json文件的列表

    # 0.创建保存转换结果的文件夹
    if (not os.path.exists(labels_dir)):
        os.mkdir(labels_dir)

    # 1.获取目录下所有的labelme标注好的Json文件，存入列表中
    for files in os.listdir(json_dir):  # 遍历json文件夹下的所有json文件
        file = os.path.join(json_dir, files)  # 获取一个json文件
        list_labels.append(file)  # 将json文件名加入到列表中

    for labels in list_labels:  # 遍历所有json文件
        with open(labels, "r") as f:
            file_in = json.load(f)
            shapes = file_in["shapes"]
            print(labels)

        txt_filename = os.path.basename(labels).replace(".json", ".txt")
        txt_path = os.path.join(labels_dir, txt_filename)  # 使用labels_dir变量指定保存路径

        with open(txt_path, "w+") as file_handle:
            for shape in shapes:
                line_content = []  # 初始化一个空列表来存储每个形状的坐标信息
                line_content.append(str(class_name.index(shape['label'])))  # 添加类别索引
                # 添加坐标信息
                for point in shape["points"]:
                    x = point[0] / file_in["imageWidth"]
                    y = point[1] / file_in["imageHeight"]
                    line_content.append(str(x))
                    line_content.append(str(y))
                # 使用空格连接列表中的所有元素，并写入文件
                file_handle.write(" ".join(line_content) + "\n")

if __name__ == "__main__":
    class_name = ['box', 'chess']
    json_dir = "/home/ubuntu/图片/labels"
    labels_dir = "/home/ubuntu/yolov8/data/labels"
    labelme2yolo_seg(class_name, json_dir, labels_dir)