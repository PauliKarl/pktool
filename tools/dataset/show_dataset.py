import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes

if __name__=='__main__':
    dataset = 'rs'
    version = 'v0'

    img_path = '/data2/pd/sdc/shipdet/{}/{}/trainval/images'.format(dataset,version)
    label_path = '/data2/pd/sdc/shipdet/{}/{}/trainval/labels'.format(dataset,version)

    for label_file in os.listdir(label_path):
        img_file = img_path + "/" + label_file.split('.txt')[0] + '.png'
        label_file = label_path + "/" + label_file

        rbboxes = []
        labels = []
        with open(label_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' ')
            points = [float(_) for _ in line[0:8]]
            rbboxes.append(points)
            labels.append(1)
        imshow_rbboxes(img_file,rbboxes,labels=labels)


