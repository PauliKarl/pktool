import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes, get_key, imshow_bboxes, pointobb2bbox, mkdir_or_exist

def imread_zh(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img


if __name__=='__main__':
    img_path = '/data/pd/hrsc2016/multiship/v1/images'
    label_path = '/data/pd/hrsc2016/multiship/v1/labels/'

    save_with_label = '/data/pd/hrsc2016/multiship/v1/showLabels'
    mkdir_or_exist(save_with_label)


    classes = {'Ship': 0, 'Frigate': 8, 'Aircraft carrier': 7, 'Cargo vessel': 2, 'Destroyer': 3, 'Warship': 1, 'Submarine': 4, 'Amphibious ship': 5, 'Cruiser': 6}


    for label_file in os.listdir(label_path):
        img_file = img_path + "/" + label_file.split('.txt')[0] + '.png'
        save_img_file = save_with_label + "/show_" + label_file.split('.txt')[0] + '.png'
        label_file = label_path + "/" + label_file
        rbboxes = []
        bboxes=[]
        labels = []

        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' ')
            points = [float(_) for _ in line[0:8]]
            rbboxes.append(pointobb2thetaobb(points))
            bboxes.append(pointobb2bbox(points))
            gt_label = " ".join(line[8:])

            labels.append(classes[gt_label])

        img = cv2.imread(img_file)

        imshow_rbboxes(img,rbboxes,labels=labels,show=False,cls_map=classes,out_file=save_with_label)

        #imshow_bboxes(img,bboxes, labels=labels,selectDir=out_file)

