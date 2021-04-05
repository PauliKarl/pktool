import os
import cv2
import numpy as np
from pktool import mkdir_or_exist, dota_parse, simpletxt_dump
import mmcv
import shutil

##########get pointobb encode of ship instances from dota-v2.0#### 
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
                    'container-crane':              None,
                    'airport':                      None,
                    'helipad':                      None}

if __name__ == "__main__":
    image_format = '.png'

    datasets = ['val','train']
    for dataset in datasets:

        origin_image_path = '/data2/pd/dota2.0/{}/images_ext/'.format(dataset)
        origin_image_path_v1 = '/data2/pd/dota1.0/{}/images/'.format(dataset)

        origin_label_path = '/data2/pd/dota2.0/{}/labelTxt-v2.0'.format(dataset)

        filtered_image_path = '/data2/pd/sdc/shipdet/dota2.0/v0/{}/images'.format(dataset)
        filtered_label_path = '/data2/pd/sdc/shipdet/dota2.0/v0/{}/labels'.format(dataset)

        mkdir_or_exist(filtered_image_path)
        mkdir_or_exist(filtered_label_path)

        filter_count = 1
        have_count = 0
        progress_bar = mmcv.ProgressBar(len(os.listdir(origin_label_path)))
        for label_name in os.listdir(origin_label_path):
            image_objects = dota_parse(os.path.join(origin_label_path, label_name))
            filtered_objects = []
            for image_object in image_objects:
                if image_object['label']=='ship':
                    have_count+=1
                    image_object['label'] = 'ship'
                    filtered_objects.append(image_object)
                else:
                    filter_count+=1
                    continue

                # if convert_classes[image_object['label']] == None:
                #     filter_count += 1
                #     continue
                # else:
                #     have_count+=1
                #     image_object['label'] = convert_classes[image_object['label']]
                #     filtered_objects.append(image_object)

            if len(filtered_objects) > 0:
                # img = cv2.imread(os.path.join(origin_image_path, os.path.splitext(label_name)[0] + image_format))
                # save_image_file = os.path.join(filtered_image_path, os.path.splitext(label_name)[0] + '.png')
                # print("Save image file: ", save_image_file)
                # cv2.imwrite(save_image_file, img)
                simpletxt_dump(filtered_objects, os.path.join(filtered_label_path, os.path.splitext(label_name)[0] + '.txt'),encode='pointobb')

                image_name = os.path.join(origin_image_path,label_name.split('.txt')[0]) + image_format
                if not os.path.isfile(image_name):
                    image_name = os.path.join(origin_image_path_v1,label_name.split('.txt')[0]) + image_format
                if os.path.isfile(image_name):
                    shutil.copy(image_name,filtered_image_path)
                    # print("copy to {}".format(filtered_image_path))
            progress_bar.update()

        print("\nFilter object counter: {}".format(filter_count))
        print("ship object counter: {}".format(have_count))