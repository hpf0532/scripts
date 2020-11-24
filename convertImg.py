# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/11/24 9:36
# file: convertImg.py
# IDE: PyCharm
from PIL import Image
import glob

# path = r'E:\0印过书的书法集\上卷\新建文件夹'
#
# file_list = glob.glob(path + r'\*.jpg')
# print(file_list)
# newImg = Image.new("RGB", (180,3543), (255,255,254))
#
# for i in file_list:
#     image = Image.open(i)
#     image.paste(newImg, (6907, 0))
#     image.paste(newImg, (0, 0))
#     image.save(i, 'JPEG')
#     print(i)
# print(len(file_list))



# image = Image.open(r"E:\0印过书的书法集\上卷\封面扉页目录\02.jpg")
#
# newImg = Image.new("RGB", (180,3543), (255,255,254))
# # for x in range(300):
# #     for y in range(300):
# #         image.putpixel((x, y), (0, 0, 255))
# image.paste(newImg,(3363,0) )
# image.paste(newImg,(0,0))
#
# # image.show()
#
# image.save(r"E:\0印过书的书法集\上卷\封面扉页目录\02.jpg", "JPEG")


class ImageHandler(object):
    def __init__(self, path):
        self.path = path
        self.padding_img = Image.new("RGB", (180,3543), (255,255,254))

    @property
    def file_list(self):
        img_list = glob.glob(self.path + r'\*.jpg')
        img_list.extend(glob.glob(self.path + r'\*.png'))
        return img_list

    def zoom(self):
        for path in self.file_list:
            im = Image.open(path)
            width, height = im.size
            if width == 7087:
                im.thumbnail((1417, 640))
            else:
                im.thumbnail((640, 640))
            print(im.format, im.size, im.mode)
            im.save(path, 'JPEG')

    def  fill(self):
        for path in self.file_list:
            im = Image.open(path)
            width, height = im.size
            if width == 7087:
                im.paste(self.padding_img, (6907, 0))
            else:
                im.paste(self.padding_img, (3363, 0))

            im.paste(self.padding_img, (0, 0))

            im.save(path, 'JPEG')
            print(im.format, im.size, im.mode)





if __name__ == '__main__':
    i = ImageHandler(r'E:\0印过书的书法集\下卷\新建文件夹')
    i.zoom()

