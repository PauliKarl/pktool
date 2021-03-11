import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes, get_key, imshow_bboxes, pointobb2bbox
def imread_zh(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img


if __name__=='__main__':
    img_path = 'F:/opticalship/dataset/18/images'
    label_path = 'F:/opticalship/dataset/18/txtlabels'

    for label_file in os.listdir(label_path):
        img_file = img_path + "/" + label_file.split('.txt')[0] + '.png'
        label_file = label_path + "/" + label_file

        rbboxes = []
        bboxes=[]
        labels = []
        tmp_classname = {}
        cls_id=0
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' ')
            points = [float(_) for _ in line[0:8]]
            rbboxes.append(pointobb2thetaobb(points))
            bboxes.append(pointobb2bbox(points))
            gt_label = " ".join(line[8:])
            if gt_label not in tmp_classname:
                tmp_classname[gt_label]=cls_id
                labels.append(cls_id)
                cls_id+=1
            else:
                labels.append(tmp_classname[gt_label])

        img = imread_zh(img_file)
        out_file = 'f:/outfile_obb_{}.png'.format(len(labels))
        imshow_rbboxes(img,rbboxes,labels=labels, selectDir=out_file)
        #imshow_bboxes(img,bboxes, labels=labels,selectDir=out_file)

