# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/12/14 11:30
# file: oss_upload.py
# IDE: PyCharm

import os
import glob
import oss2
import sys


end_point = "http://oss-cn-beijing.aliyuncs.com"
bucket_name = "yidunbucket"
class OSSUtils(object):
    count = 0
    def __init__(self, access_key_id, access_key_secret, ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, end_point, bucket_name)


    def upload(self, file):
        obj_name = "yd_service/2020/12/"+ os.path.split(file)[-1]

        # with open(file, 'rb') as fileobj:
        #     # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
        #     fileobj.seek(1000, os.SEEK_SET)
        #     # Tell方法用于返回当前位置。
        #     current = fileobj.tell()
        #     self.bucket.put_object(obj_name, fileobj)
        try:
            if self.bucket.object_exists(obj_name):
                print("文件存在")
                self.bucket.put_object_from_file(obj_name, file)
                self.count += 1
                print("{0} 文件{1}上传成功".format(self.count, file))
            else:
                print("文件不存在")

        except Exception as e:
            print("文件{}上传失败".format(file), e)
            with open(r'E:\error.log', 'w+') as f:
                f.write("文件{}上传失败".format(file))



if __name__ == '__main__':
    # pdf_file_list = glob.glob(r'E:\yingtan20201211002管辖变更补充协议\*\*.pdf')
    # print(pdf_file_list)
    # file = 'E:\\yingtan20201211002管辖变更补充协议\\1-MTYILSHD20190108300554080270-冯京\\1-MTYILSHD20190108300554080270-冯京-鹰潭管辖变更补充协议.pdf'
    # obj_name = "yd_service/2020/12/" + os.path.split(file)[-1]
    # print(obj_name)
    #
    # a, b = os.path.split(file)
    # print(a,b)

    pass