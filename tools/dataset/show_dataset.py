import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes

if __name__=='__main__':
    #['dota2.0','hrsc2016','rs','fair1m']
    #datasets=['test','trainval']
    sdc_type = 'multidet'
    dataset_type = '/'
    dataset = 'trainval'
    version = 'v0'

    img_path = '/data2/pd/sdc/{}/{}/{}/{}/images'.format(sdc_type,dataset_type,version,dataset)
    label_path = '/data2/pd/sdc/{}/{}/{}/{}/labels'.format(sdc_type,dataset_type,version,dataset)


    cls_map = {}
    clsID=0
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
            label = " ".join(line[8:])
            if label in cls_map:
                label = cls_map[label]
            else:
                cls_map[label]=clsID+1
                label = clsID+1
                clsID+=1
            rbboxes.append(points)
            labels.append(label)
        print(img_file)

        imshow_rbboxes(img_file,rbboxes,labels=labels)



