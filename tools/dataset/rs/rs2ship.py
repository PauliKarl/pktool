r'''dataset infos see https://github.com/lllltdaf2/Ship-Seg-Detect-data
'''
import os
import cv2
import numpy as np
from pktool import mkdir_or_exist, simpletxt_dump, pointobb2thetaobb
import math

def parse_rs_txt(labelFile):
    """parse RS-ship-dataset annotation file
    return specimens
    """
    with open(labelFile, 'r') as f:
        lines = f.readlines()
    
    specimens = []
    for line in lines:
        line = line.rstrip().split(' ')
        specimen = {}
        shapes = []

        specimen['image_id'] = line[0].split('.bmp')[0]
        ship_num = int(line[1])
        for i in range(ship_num):
            point = [0,0,0,0,0,0,0,0]
            point[::2] = [float(_) for _ in line[2+15*i:6+15*i]]
            point[1::2] = [float(_) for _ in line[7+15*i:11+15*i]]
            shapes.append(point)
        specimen['ships']=shapes
        specimens.append(specimen)

    return specimens

if __name__=='__main__':
    labeltxt='/data/zrx/ShipDetection/RS-shipdata/GoogleEarth/RotationRegionLabels.txt'
    imageFolder = '/data/zrx/ShipDetection/RS-shipdata/images/'
    specimens=parse_rs_txt(labeltxt)

    filtered_image_path = '/data2/pd/sdc/shipdet/rs/v0/trainval/images/'
    filtered_label_path = '/data2/pd/sdc/shipdet/rs/v0/trainval/labels'

    mkdir_or_exist(filtered_image_path)
    mkdir_or_exist(filtered_label_path)

    max_length = 0
    min_length = 102424
    for specimen in specimens:
        filtered_objects=[]

        image_id = specimen['image_id']
        ships = specimen['ships']
        for ship in ships:
            filtered_object = {}
            filtered_object['label']='ship'
            filtered_object['points']=ship
            filtered_objects.append(filtered_object)
        label_save_file = os.path.join(filtered_label_path,image_id+'.txt')
        simpletxt_dump(filtered_objects,label_save_file,encode='points')

        OriImgName = imageFolder+image_id+'.png'
        TarImgName = filtered_image_path+image_id+'.png'

        img=cv2.imread(OriImgName)
        # print(OriImgName)
        height, width = img.shape[0],img.shape[1]
        max_length = max(max_length,height,width)
        min_length = min(min_length,height,width)

        cv2.imwrite(TarImgName, img)
        print("{}:save as {} and {}".format(image_id,label_save_file,image_id+'.png'))
        
    print(max_length,min_length)  


        








