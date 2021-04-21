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

    # CLASSES=('Cargo vessel','Ship','Motorboat','Fishing boat','Destroyer','Tugboat','Loose pulley','Warship','Engineering ship','Amphibious ship','Cruiser','Frigate','Submarine','Aircraft carrier','Hovercraft','Command ship')
    CLASSES=('ship',)
    img_path = '/data2/pd/sdc/shipdet/v1/coco/test/'
    label_path = '/data2/pd/sdc/shipdet/v1/works_dir/aedet/faster_rcnn_RoITrans_r50_fpn_1x_shipdet/Task1_results_nms/'
    #'/home/pd/AerialDetection/work_dirs/sdc/faster_rcnn_obb_r50_fpn_1x_sdc/Task1_results_nms/person.txt'
    save_img_res = '/data2/pd/sdc/shipdet/v1/works_dir/aedet/faster_rcnn_RoITrans_r50_fpn_1x_shipdet/res_img_no_label/'
    results = {}
    for cat in CLASSES:
        result_txt = label_path + cat + '.txt'
        with open(result_txt,'r') as f:
            lines = f.readlines()
            splitlines = [x.strip().split(' ') for x in lines]
            for splitline in splitlines:
                if splitline[0] not in results:
                    results[splitline[0]] = [[],[]]
                else:
                    results[splitline[0]][0].append(float(splitline[1]))
                    results[splitline[0]][1].append([float(ponit) for ponit in splitline[2:]])


        for imgName,result in results.items():
            img_file = img_path + imgName +''#'.png'
            out_img_res = save_img_res + imgName

            points = []
            scores = []
            labels = []
            scores, points=result[0],result[1]
            # scores = [map(float,score) for score in scores]

            labels = [1 for i in scores]
            print(img_file)
            imshow_rbboxes(img_file,points,labels=labels,show_label=False,out_file=out_img_res,show=False)


