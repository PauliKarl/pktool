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

        # labels=('Cargo vessel','Ship','Motorboat','Fishing boat','Destroyer','Tugboat','Loose pulley','Warship','Engineering ship','Amphibious ship','Cruiser','Frigate','Submarine','Aircraft carrier','Command ship','Hovercraft')
        # Tval = (5529,2927,2610,1414,799,660,628,526,507,485,449,400,346,302,142,126)
        # colors = ('blue','green','yellow','purple','cyan','brown','Red','orange','magenta','Lime','Teal','Maroon','#808080','#FFD7B4','#FFFAC8','#808000')
        classes = {'Cargo vessel':1,'Ship':2,'Motorboat':3,'Fishing boat':4,'Destroyer':5,'Tugboat':6,'Loose pulley':7,'Warship':8,'Engineering ship':9,'Amphibious ship':10,'Cruiser':11,'Frigate':12,'Submarine':13,'Aircraft carrier':14,'Command ship':15,'Hovercraft':16}

        colors_map = ['black','blue','green','yellow','purple','cyan','brown','Red','orange','magenta','Lime','Teal','Maroon','Grey','Apricot','Beige','Olive']

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

