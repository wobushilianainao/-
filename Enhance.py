import xml.etree.ElementTree as ET
import os
import numpy as np
from PIL import Image
import shutil
import imgaug as ia
from imgaug import augmenters as iaa
from tqdm import tqdm


# 作用：
# 这段代码主要是通过遍历 XML 文件的节点结构，提取出物体边界框（bounding box）的坐标信息，并将其存储在列表中返回。
# 同时，代码中运用了 Python 中的 os 模块来处理文件路径，以及使用了 ElementTree 模块（一般通过
# import xml.etree.ElementTree as ET 导入）来解析 XML 文件。
def read_xml_annotation(root, image_id):
    # 使用 open 函数来打开 XML 文件，文件路径是 root 和 image_id 的组合，使用 UTF-8 编码方式
    in_file = open(os.path.join(root, image_id), encoding='UTF-8')
    tree = ET.parse(in_file) #使用 ET.parse 函数来解析 XML 文件，获取 XML 文件的树结构。
    root = tree.getroot()  #获取 XML 文件的根节点。
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有名字为’country‘的节点
        bndbox = object.find('bndbox')  # 获取每个 ‘object’ 节点下的 ‘bndbox’ 子节点
        xmin = int(bndbox.find('xmin').text) #获取 ‘bndbox’ 子节点下的 ‘xmin’ 节点的文本内容并转换为整数，依次获取其他边界框坐标信息。
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
    return bndboxlist


#作用：
# 这段代码的主要作用是根据传入的新的物体边界框信息列表 new_target，
# 修改原始的 XML 文件中的物体边界框信息，然后保存为新的 XML 文件
def change_xml_list_annotation(root, image_id, new_target, saveroot, xml_id):
    save_path = os.path.join(saveroot, xml_id) #拼接保存路径
    in_file = open(os.path.join(root, str(image_id) + '.xml'), encoding='UTF-8')  # 这里root分别由两个意思
    tree = ET.parse(in_file) #使用 ET.parse 函数来解析 XML 文件，获取 XML 文件的树结构。
    elem = tree.find('filename')
    elem.text = xml_id + img_type #修改 ‘filename’ 节点的文本内容，将其设为 xml_id 加上 img_type。
    xmlroot = tree.getroot() #获取 XML 文件的根节点。
    index = 0

    for object in xmlroot.findall('object'):  # 找到xmlroot节点下的所有名为’country‘的节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index += 1

    tree.write(save_path + '.xml') #


# AUG_IMG_DIR：存储增强后的影像文件地址
# AUGLOOP：增强倍数
# IMG_DIR：原照片地址
# XML_DIR：原xml文件地址
# AUG_XML_DIR：增强后的xml文件地址
def simple_example(AUGLOOP,IMG_DIR,XML_DIR,AUG_IMG_DIR,AUG_XML_DIR):
    boxes_img_aug_list = []
    new_bndbox_list = []
    new_name = None

    for root, sub_folders, files in os.walk(XML_DIR):  #使用 os.walk 遍历 XML_DIR 目录下的文件。
        for name in tqdm(files):   # 对遍历到的每个文件名进行迭代，使用 tqdm 来显示进度条。
            bndbox = read_xml_annotation(XML_DIR, name) #调用 read_xml_annotation 函数来读取 XML 注释文件中的边界框信息。
            shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR) #将当前XML文件 复制到 新的XML目录中。

        # 尝试将相应的图像文件从原始图像目录复制到增强后的图像目录。如果出现异常，则将.JPG格式的图像复制到增强后的目录。
        #这里的[:-4]表示从字符串的开头开始切片，直到倒数第四个字符之前（不包括倒数第四个字符），因此它实际上是将字符串的后缀（比如文件的扩展名）去掉。
            try:
                shutil.copy(os.path.join(IMG_DIR, name[:-4] + img_type), AUG_IMG_DIR)
            except:
                shutil.copy(os.path.join(IMG_DIR, name[:-4] + '.JPG'), AUG_IMG_DIR)
            # print(os.path.join(IMG_DIR, name[:-4] + img_type))

            for epoch in range(1, AUGLOOP + 1):
                # 增强
                if epoch == 1:
                    seq = iaa.Sequential([
                        ####0.75-1.5随机数值为alpha，对图像进行对比度增强，该alpha应用于每个通道
                        iaa.ContrastNormalization((0.75, 1.5), per_channel=True),
                    ])
                elif epoch == 2:
                    seq = iaa.Sequential([
                        #### loc 噪声均值，scale噪声方差，50%的概率，对图片进行添加白噪声并应用于每个通道
                        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.1 * 255), per_channel=0.75),
                    ])
                elif epoch == 3:
                    seq = iaa.Sequential([
                        iaa.Fliplr(1),  # 水平镜像翻转
                    ])
                elif epoch == 4:
                    seq = iaa.Sequential([
                        iaa.Affine(rotate=90) # 翻转90度
                    ])
                elif epoch == 5:
                    seq = iaa.Sequential([
                         iaa.Affine(rotate=180)  # 翻转180度
                    ])
                elif epoch == 6:
                    seq = iaa.Sequential([
                        iaa.Affine(rotate=270)])  # 翻转270度

                seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
                # 读取图片
                try:
                    img = Image.open(os.path.join(IMG_DIR, name[:-4] + img_type))
                except:
                    img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.JPG'))

                # JPG不支持alpha透明度，有可能报RGBA错误，将图片丢弃透明度转成RGB
                img = img.convert('RGB')
                # sp = img.size
                img = np.asarray(img) #并将其转换为 NumPy 数组
                # bndbox 坐标增强
                for i in range(len(bndbox)):
                    #将边界框坐标转换为 imgaug 库中的 BoundingBoxesOnImage 对象。
                    bbs = ia.BoundingBoxesOnImage([
                        ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                    ], shape=img.shape)

                    #对边界框进行增强，并将增强后的边界框添加到列表 boxes_img_aug_list 中。
                    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                    boxes_img_aug_list.append(bbs_aug)

                    # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                    n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                    n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                    n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                    n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                    if n_x1 == 1 and n_x1 == n_x2:
                        n_x2 += 1
                    if n_y1 == 1 and n_y2 == n_y1:
                        n_y2 += 1
                    if n_x1 >= n_x2 or n_y1 >= n_y2:
                        print('error', name)
                    new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])

                    # 存储变化后的图片
                    image_aug = seq_det.augment_images([img])[0]
                    # 新文件名
                    new_name = name[:-4] + '-' + str(epoch)
                    path = os.path.join(AUG_IMG_DIR, new_name + img_type)

                    image_auged = bbs.draw_on_image(image_aug, thickness=0)
                    Image.fromarray(image_auged).save(path)

                # 存储变化后的XML
                change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR, new_name)
                new_bndbox_list = []


if __name__ == "__main__":

    # 随机种子
    ia.seed(1)
    img_type = '.jpg'
    # img_type = '.png'

    # 原数据路径
    IMG_DIR = "E:/Desktop/testt/image"
    XML_DIR = "E:/Desktop/testt/xml"

    # 存储增强后的影像文件夹路径
    AUG_IMG_DIR = "E:/Desktop/testt/new_img/"
    if not os.path.exists(AUG_IMG_DIR):
        os.mkdir(AUG_IMG_DIR)

    # 存储增强后的XML文件夹路径
    AUG_XML_DIR = "E:/Desktop/testt/new_xml/"
    if not os.path.exists(AUG_XML_DIR):
        os.mkdir(AUG_XML_DIR)

    # 数据增强n倍
    simple_example(6, IMG_DIR, XML_DIR, AUG_IMG_DIR, AUG_XML_DIR)

