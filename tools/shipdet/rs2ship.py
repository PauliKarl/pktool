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
            shapes.append(pointobb2thetaobb(point))
        specimen['ships']=shapes
        specimens.append(specimen)

    return specimens

if __name__=='__main__':
    labeltxt='/data/zrx/ShipDetection/RS-shipdata/GoogleEarth/RotationRegionLabels.txt'
    imageFolder = '/data/zrx/ShipDetection/RS-shipdata/images/'
    specimens=parse_rs_txt(labeltxt)

    filtered_image_path = '/data/pd/rs/ship/v0/images'
    filtered_label_path = '/data/pd/rs/ship/v0/labels'
    mkdir_or_exist(filtered_image_path)
    mkdir_or_exist(filtered_label_path)

    for specimen in specimens:
        filtered_objects=[]

        image_id = specimen['image_id']
        ships = specimen['ships']
        for ship in ships:
            filtered_object = {}
            filtered_object['label']='ship'
            filtered_object['theta']=ship
            filtered_objects.append(filtered_object)
        label_save_file = os.path.join(filtered_label_path,image_id+'.txt')
        simpletxt_dump(filtered_objects,label_save_file,encode='theta')
        print("{}:save as {}".format(image_id,label_save_file))
        


        








