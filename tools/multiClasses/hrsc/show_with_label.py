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

    datasets= ['test','trainval']
    for dataset in datasets:
        img_path = '/data2/pd/sdc/multidet/v0/{}/images/'.format(dataset)
        label_path = '/data2/pd/sdc/multidet/v0/{}/labels/'.format(dataset)

        save_with_label = '/data2/pd/sdc/multidet/v0/{}_show_bbox/'.format(dataset)
        mkdir_or_exist(save_with_label)


        classes = {'Ship': 1, 'Destroyer': 2,'Cargo vessel': 3,'Amphibious ship': 4,'Cruiser': 5,'Frigate':6,'Warship': 7, 'Submarine': 8, 'Aircraft carrier': 9, 'Command ship':10,'Hovercraft':11,'Loose pulley':12}

        colors_map = ['black','blue','green','yellow','purple','cyan','brown','red','orange','magenta','Lime','Teal','Maroon']
        # plt.bar(1, 1693, label='Other ship',color='blue')
        # plt.bar(2, 820, label='Destroyer',color='green')
        # plt.bar(3, 697, label='Cargo vessel', color='yellow')
        # plt.bar(4, 485, label='Amphibious ship',color='purple')
        # plt.bar(5, 450, label='Cruiser',color='cyan')
        # plt.bar(6, 400, label='Frigate',color='brown')
        # plt.bar(7, 376, label='Warship',color='red')
        # plt.bar(8, 358, label='Submarine',color='orange')
        # plt.bar(9, 302, label='Aircraft carrier',color='magenta')
        # plt.bar(10, 142, label='Command ship',color='Lime')
        # plt.bar(11, 126, label='Hovercraft',color='Teal')
        # plt.bar(12, 16, label='Loose pulley',color='Maroon')

        for label_file in os.listdir(label_path):
            img_file = img_path + "/" + label_file.split('.txt')[0] + '.png'
            save_img_file = save_with_label + label_file.split('.txt')[0] + '.png'
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

            imshow_rbboxes(img,rbboxes,labels=labels,colors_map=colors_map,show=False,cls_map=classes,out_file=save_img_file)

            #imshow_bboxes(img,bboxes, labels=labels,selectDir=out_file)

