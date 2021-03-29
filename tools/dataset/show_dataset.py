import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes

if __name__=='__main__':
    #['dota2.0','hrsc2016','rs']
    #datasets=['test','trainval']
    dataset_type = 'dota2.0'
    dataset = 'trainval'
    version = 'v1'

    img_path = '/data2/pd/sdc/shipdet/{}/{}/{}/images'.format(dataset_type,version,dataset)
    label_path = '/data2/pd/sdc/shipdet/{}/{}/{}/labels'.format(dataset_type,version,dataset)

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
        print(img_file)
        imshow_rbboxes(img_file,rbboxes,labels=labels)



