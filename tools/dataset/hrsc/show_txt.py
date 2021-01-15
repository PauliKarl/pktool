import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes, get_key

if __name__=='__main__':
    img_path = '/data/pd/hrsc2016/v0/test//images/'
    label_path = '/data/pd/hrsc2016/v0/test/annotations/'

    for label_file in os.listdir(label_path):
        img_file = img_path + "/" + label_file.split('.txt')[0] + '.bmp'
        label_file = label_path + "/" + label_file

        rbboxes = []
        labels = []
        tmp_classname = {}
        cls_id=0
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' ')
            robndbox = [float(_) for _ in line[0:5]]
            rbboxes.append(robndbox)
            gt_label = " ".join(line[5:])
            if gt_label not in tmp_classname:
                tmp_classname[gt_label]=cls_id
                labels.append(cls_id)
                cls_id+=1
            else:
                labels.append(tmp_classname[gt_label])
        print(tmp_classname)
        imshow_rbboxes(img_file,rbboxes,labels=labels, show_label=True)