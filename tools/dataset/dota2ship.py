import os
import cv2
import numpy as np
from pktool import mkdir_or_exist, dota_parse, simpletxt_dump
import mmcv

##########get pointobb encode of ship instances from dota-v1.5#### 
convert_classes = { 'harbor':                       None, 
                    'ship':                         'ship', 
                    'small-vehicle':                None, 
                    'large-vehicle':                None, 
                    'storage-tank':                 None, 
                    'plane':                        None, 
                    'soccer-ball-field':            None, 
                    'bridge':                       None, 
                    'baseball-diamond':             None, 
                    'tennis-court':                 None, 
                    'helicopter':                   None, 
                    'roundabout':                   None, 
                    'swimming-pool':                None, 
                    'ground-track-field':           None, 
                    'basketball-court':             None,
                    'container-crane':              None}

if __name__ == "__main__":
    image_format = '.png'

    origin_image_path = '/data/dota/origin/train/images/'
    origin_label_path = '/data/dota/origin/train/labelTxt-v1.5'

    filtered_image_path = '/data/pd/dota-v1.5/ship/v0/images'
    filtered_label_path = '/data/pd/dota-v1.5/ship/v0/labels'

    mkdir_or_exist(filtered_image_path)
    mkdir_or_exist(filtered_label_path)

    filter_count = 1
    progress_bar = mmcv.ProgressBar(len(os.listdir(origin_label_path)))
    for label_name in os.listdir(origin_label_path):
        image_objects = dota_parse(os.path.join(origin_label_path, label_name))
        filtered_objects = []
        for image_object in image_objects:
            if convert_classes[image_object['label']] == None:
                filter_count += 1
                continue
            else:
                image_object['label'] = convert_classes[image_object['label']]
                filtered_objects.append(image_object)

        if len(filtered_objects) > 0:
            # img = cv2.imread(os.path.join(origin_image_path, os.path.splitext(label_name)[0] + image_format))
            # save_image_file = os.path.join(filtered_image_path, os.path.splitext(label_name)[0] + '.png')
            # print("Save image file: ", save_image_file)
            # cv2.imwrite(save_image_file, img)
            simpletxt_dump(filtered_objects, os.path.join(filtered_label_path, os.path.splitext(label_name)[0] + '.txt'),encode='pointobb')
        
        progress_bar.update()

    print("Filter object counter: {}".format(filter_count))