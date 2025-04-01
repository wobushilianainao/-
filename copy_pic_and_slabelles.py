import glob
import random
from PIL import Image, ImageDraw, ImageFont
import sys
import os
import time

global classes,x,y,w,h,line,lines,i,txtname,num_change,txtpath,jpgpath

def turn_clockwise0():
    wtxtname = f"{txtname.replace(txtpath,f'{txtpath}/copies').split('.')[0]}_{i}.txt"
    jpgname = f"{txtname.replace(txtpath,jpgpath).split('.')[0]}.jpg"
    wjpgname = f"{txtname.replace(txtpath,f'{jpgpath}/copies').split('.')[0]}_{i}.jpg"
    with open(txtname, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines :
        classes,x,y,w,h = line.strip().split()
        wclasses = int(classes)
        wx = float(x)
        wy = float(y)
        ww = float(w)
        wh = float(h)
        
        new_line = f"{wclasses} {wx:.6f} {wy:.6f} {ww:.6f} {wh:.6f}\n"
        new_lines.append(new_line)
    with open(wtxtname, 'w') as file:
        file.writelines(new_lines)
        print(f'{str(new_lines)}已写入进(new txt has been created){str(wtxtname)}')
    with Image.open(jpgname) as img:
        # 顺时针旋转90度
        rotated = img#.rotate(0, expand=True)
        '''
        draw = ImageDraw.Draw(rotated)
        draw.text((10,10),"顺时针旋转0°(turn 0)", fill=(255, 255, 255), font=ImageFont.truetype('simhei.ttf', size=20))
        '''
        # 保存旋转后的图像
        rotated.save(wjpgname)
        print(f'图像已旋转并创建(new jpg has been created){str(wjpgname)}')

def turn_clockwise90():
    wtxtname = f"{txtname.replace(txtpath,f'{txtpath}/copies').split('.')[0]}_{i}.txt"
    jpgname = f"{txtname.replace(txtpath,jpgpath).split('.')[0]}.jpg"
    wjpgname = f"{txtname.replace(txtpath,f'{jpgpath}/copies').split('.')[0]}_{i}.jpg"
    with open(txtname, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines :
        classes,x,y,w,h = line.strip().split()
        wclasses = int(classes)
        wy = float(x)
        wx = 1 - float(y)
        ww = float(h)
        wh = float(w)
        
        new_line = f"{wclasses} {wx:.6f} {wy:.6f} {ww:.6f} {wh:.6f}\n"
        new_lines.append(new_line)
    with open(wtxtname, 'w') as file:
        file.writelines(new_lines)
        print(f'{str(new_lines)}已写入进(new txt has been created){str(wtxtname)}')
    
    with Image.open(jpgname) as img:
        # 顺时针旋转90度
        rotated = img.rotate(-90, expand=True)
        '''
        draw = ImageDraw.Draw(rotated)
        draw.text((10,10),"顺时针旋转90°(turn π/2)", fill=(255, 255, 255), font=ImageFont.truetype('simhei.ttf', size=20))
        '''
        # 保存旋转后的图像
        rotated.save(wjpgname)
        print(f'图像已旋转并创建(new jpg has been created){str(wjpgname)}')

def turn_clockwise180():
    wtxtname = f"{txtname.replace(txtpath,f'{txtpath}/copies').split('.')[0]}_{i}.txt"
    jpgname = f"{txtname.replace(txtpath,jpgpath).split('.')[0]}.jpg"
    wjpgname = f"{txtname.replace(txtpath,f'{jpgpath}/copies').split('.')[0]}_{i}.jpg"
    with open(txtname, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines :
        classes,x,y,w,h = line.strip().split()
        wclasses = int(classes)
        wx = 1 - float(x)
        wy = 1 - float(y)
        ww = float(w)
        wh = float(h)
        
        new_line = f"{wclasses} {wx:.6f} {wy:.6f} {ww:.6f} {wh:.6f}\n"
        new_lines.append(new_line)
    with open(wtxtname, 'w') as file:
        file.writelines(new_lines)
        print(f'{str(new_lines)}已写入进(new txt has been created){str(wtxtname)}')
    
    with Image.open(jpgname) as img:
        # 顺时针旋转90度
        rotated = img.rotate(-180, expand=True)
        '''
        draw = ImageDraw.Draw(rotated)
        draw.text((10,10),"顺时针旋转180°(turn π)", fill=(255, 255, 255), font=ImageFont.truetype('simhei.ttf', size=20))
        '''
        # 保存旋转后的图像
        rotated.save(wjpgname)
        print(f'图像已旋转并创建(new jpg has been created){str(wjpgname)}')

def turn_clockwise270():
    wtxtname = f"{txtname.replace(txtpath,f'{txtpath}/copies').split('.')[0]}_{i}.txt"
    jpgname = f"{txtname.replace(txtpath,jpgpath).split('.')[0]}.jpg"
    wjpgname = f"{txtname.replace(txtpath,f'{jpgpath}/copies').split('.')[0]}_{i}.jpg"
    with open(txtname, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines :
        classes,x,y,w,h = line.strip().split()
        wclasses = int(classes)
        wx = float(y)
        wy = 1 - float(x)
        ww = float(h)
        wh = float(w)
        
        new_line = f"{wclasses} {wx:.6f} {wy:.6f} {ww:.6f} {wh:.6f}\n"
        new_lines.append(new_line)
    with open(wtxtname, 'w') as file:
        file.writelines(new_lines)
        print(f'{str(new_lines)}已写入进(new txt has been created){str(wtxtname)}')
    
    with Image.open(jpgname) as img:
        # 顺时针旋转90度
        rotated = img.rotate(-270, expand=True)
        '''
        draw = ImageDraw.Draw(rotated)
        draw.text((10,10),"顺时针旋转270°(turn 3π/2)", fill=(255, 255, 255), font=ImageFont.truetype('simhei.ttf', size=20))
        '''
        # 保存旋转后的图像
        rotated.save(wjpgname)
        print(f'图像已旋转并创建(new jpg has been created){str(wjpgname)}')

def x_overturn():
    wtxtname = f"{txtname.replace(txtpath,f'{txtpath}/copies').split('.')[0]}_{i}.txt"
    jpgname = f"{txtname.replace(txtpath,jpgpath).split('.')[0]}.jpg"
    wjpgname = f"{txtname.replace(txtpath,f'{jpgpath}/copies').split('.')[0]}_{i}.jpg"
    with open(txtname, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines :
        classes,x,y,w,h = line.strip().split()
        wclasses = int(classes)
        wx = float(x)
        wy = 1 -float(y)
        ww = float(w)
        wh = float(h)
        
        new_line = f"{wclasses} {wx:.6f} {wy:.6f} {ww:.6f} {wh:.6f}\n"
        new_lines.append(new_line)
    with open(wtxtname, 'w') as file:
        file.writelines(new_lines)
        print(f'{str(new_lines)}已写入进(new txt has been created){str(wtxtname)}')
    
    with Image.open(jpgname) as img:
        # 顺时针旋转90度
        rotated = img.transpose(Image.FLIP_TOP_BOTTOM)
        '''
        draw = ImageDraw.Draw(rotated)
        draw.text((10,10),"横向翻转(overturn broadwise)", fill=(255, 255, 255), font=ImageFont.truetype('simhei.ttf', size=20))
        '''
        # 保存旋转后的图像
        rotated.save(wjpgname)
        print(f'图像已旋转并创建(new jpg has been created){str(wjpgname)}')

def y_overturn():
    wtxtname = f"{txtname.replace(txtpath,f'{txtpath}/copies').split('.')[0]}_{i}.txt"
    jpgname = f"{txtname.replace(txtpath,jpgpath).split('.')[0]}.jpg"
    wjpgname = f"{txtname.replace(txtpath,f'{jpgpath}/copies').split('.')[0]}_{i}.jpg"
    with open(txtname, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines :
        classes,x,y,w,h = line.strip().split()
        wclasses = int(classes)
        wx = 1 - float(x)
        wy = float(y)
        ww = float(w)
        wh = float(h)
        
        new_line = f"{wclasses} {wx:.6f} {wy:.6f} {ww:.6f} {wh:.6f}\n"
        new_lines.append(new_line)
    with open(wtxtname, 'w') as file:
        file.writelines(new_lines)
        print(f'{str(new_lines)}已写入进(new txt has been created){str(wtxtname)}')
    
    with Image.open(jpgname) as img:
        # 顺时针旋转90度
        rotated = img.transpose(Image.FLIP_LEFT_RIGHT)
        '''
        draw = ImageDraw.Draw(rotated)
        draw.text((10,10),"纵向翻转(overturn vertically)", fill=(255, 255, 255), font=ImageFont.truetype('simhei.ttf', size=20))
        '''
        # 保存旋转后的图像
        rotated.save(wjpgname)
        print(f'图像已旋转并创建(new jpg has been created){str(wjpgname)}')

txtpath = input(f"输入你的标注文件（path of *.txt）目录：")
jpgpath = input(f"输入你的图片（path of *.jpg）目录：")
num_change = input("请输入需要的倍数(copy times): ")
txt_num = len(glob.glob(f'{txtpath}/*.txt'))
jpg_nmu = len(glob.glob(f'{jpgpath}/*.jpg'))
os.makedirs(f'{txtpath}/copies',exist_ok=True)
os.makedirs(f'{jpgpath}/copies',exist_ok=True)

if txt_num == jpg_nmu:
    for txtname in glob.glob(f'{txtpath}/*.txt'):
        # 打开文件并逐行读取
        with open(txtname, 'r') as file:
            lines = file.readlines()
        print(f"{txtname}的标注数量(number of labells)：{len(lines)}")
        for i in range(int(num_change) + 1):
            choices = random.choice([1,2,3,4,5,6])
            if choices == 1:
                turn_clockwise0()
            elif choices == 2:
                turn_clockwise90()
            elif choices == 3:
                turn_clockwise180()
            elif choices == 4:
                turn_clockwise270()
            elif choices == 5:
                x_overturn()
            elif choices == 6:
                y_overturn()
            #time.sleep(0.1)
                
else:
    print(f'图片数量(num of *.jpg):{jpg_nmu}')
    print(f'标注信息数量(num of *.txt):{txt_num}')
    print("标注信息数量和图片数量不一致！(different number of *.txt and *.jpg)")
    print("请不要将classes.txt放在标注信息目录中(do not put classes.txt in labells path)")
    sys.exit()
        
        