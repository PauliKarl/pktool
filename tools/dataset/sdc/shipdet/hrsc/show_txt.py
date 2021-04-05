import numpy as np
import random
import six
import cv2
import os
from pktool import  imshow_rbboxes, get_key

if __name__=='__main__':
    img_path = '/data/hrsc2016/release/v0/trainval/images/'
    label_path = '/data2/pd/sdc/shipdet/hrsc2016/v0/trainval/labels'

    for label_file in os.listdir(label_path):
        img_file = img_path + "/" + label_file.split('.txt')[0] + '.bmp'
        label_file = label_path + "/" + label_file

        bboxes = []
        labels = []
        tmp_classname = {}
        cls_id=0
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' ')
            robndbox = [float(_) for _ in line[0:8]]
            bboxes.append(robndbox)
            gt_label = " ".join(line[8:])
            if gt_label not in tmp_classname:
                tmp_classname[gt_label]=cls_id
                labels.append(cls_id)
                cls_id+=1
            else:
                labels.append(tmp_classname[gt_label])
        print(img_file)
        # img = cv2.imread(img_file)
        # print(label_file)
        imshow_rbboxes(img_file,bboxes,labels=labels, show_label=True)