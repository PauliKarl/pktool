import numpy as np
import random
import six
import cv2
import os
from pktool import  imshow_rbboxes

if __name__=='__main__':
    img_path = '/data/pd/rs/ship/v0/images'
    label_path = '/data/pd/rs/ship/v0/labels'

    for label_file in os.listdir(label_path):
        img_file = img_path + "/" + label_file.split('.txt')[0] + '.png'
        label_file = label_path + "/" + label_file

        rbboxes = []
        labels = []
        with open(label_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' ')
            theta = [float(_) for _ in line[0:5]]
            rbboxes.append(theta)
            labels.append(1)
        imshow_rbboxes(img_file,rbboxes,labels=labels)


