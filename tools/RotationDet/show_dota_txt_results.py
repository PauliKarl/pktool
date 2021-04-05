import numpy as np
import random
import six
import cv2
import os
from pktool import  pointobb2thetaobb, imshow_rbboxes

if __name__=='__main__':
    r"""txt format:
    for each line: P1062__0_824.png 0.9927523136138916 985.03271484375 615.8108520507812 997.364990234375 614.2393188476562 1000.8902587890625 641.9028930664062 988.5579833984375 643.4744262695312
    info:imageName(str) confidence(1 float) pointobbs(8 float)
    """
    img_path = '/data2/pd/sdc/shipdet/v0/coco/test/'
    label_path = '/home/pd/RotationDetection/tools/scrdet/test_dota/FPN_Res50_DOTA2.0_1x_20201103/dota_res_r/Task1_ship.txt'
    #'/home/pd/AerialDetection/work_dirs/sdc/faster_rcnn_obb_r50_fpn_1x_sdc/Task1_results_nms/person.txt'

    results = {}
    with open(label_path,'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split(' ') for x in lines]
        for splitline in splitlines:
            if splitline[0] not in results:
                results[splitline[0]] = [[],[]]
            else:
                results[splitline[0]][0].append(float(splitline[1]))
                results[splitline[0]][1].append([float(ponit) for ponit in splitline[2:]])


    for imgName,result in results.items():
        img_file = img_path + imgName +'.png'

        points = []
        scores = []
        labels = []
        scores, points=result[0],result[1]
        # scores = [map(float,score) for score in scores]

        labels = [1 for i in scores]
        imshow_rbboxes(img_file,points,labels=labels,scores=scores)


