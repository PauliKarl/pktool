import argparse

import os
import cv2
import json
import numpy as np

import mmcv
from pktool import Convert2COCO

class xView2COCO(Convert2COCO):
    def __generate_coco_annotation__(self, annotpath, imgpath):
        """
        docstring here
            :param self: 
            :param annotpath: the path of each annotation
            :param return: dict()  
        """
        objects = self.__simpletxt_parse__(annotpath)
        
        coco_annotations = []
        
        for object_struct in objects:
            bbox = object_struct['bbox']
            label = object_struct['label']

            width = bbox[2]
            height = bbox[3]
            area = height * width

            if area <= self.small_object_area and self.groundtruth:
                self.small_object_idx += 1
                continue

            coco_annotation = {}
            coco_annotation['bbox'] = bbox
            coco_annotation['category_id'] = label
            coco_annotation['area'] = np.float(area)
            coco_annotation['num_keypoints'] = 4

            coco_annotations.append(coco_annotation)
            
        return coco_annotations
    
    def __simpletxt_parse__(self, label_file):

        objects = []
        if self.groundtruth:
            lines = open(label_file, 'r').readlines()
            for line in lines:
               
                obj_struct = {}
                xyxy2 = [float(xy) for xy in line.rstrip().split(' ')[:4]]
                
                gt_label = " ".join(line.rstrip().split(' ')[4:])

                xmin = min(xyxy2[0::2])
                ymin = min(xyxy2[1::2])
                xmax = max(xyxy2[0::2])
                ymax = max(xyxy2[1::2])
                bbox_w = xmax - xmin
                bbox_h = ymax - ymin
                obj_struct['bbox'] = [xmin, ymin, bbox_w, bbox_h]
                obj_struct['label'] = original_class[gt_label]

                objects.append(obj_struct)
        else:
            obj_struct = {}
            obj_struct['bbox'] = [0, 0, 0, 0]
            obj_struct['label'] = 0
            objects.append(obj_struct)
        return objects

def parse_args():
    parser = argparse.ArgumentParser(description='MMDet test detector')
    parser.add_argument(
        '--imagesets',
        type=str,
        nargs='+',
        choices=['trainval', 'test'])
    parser.add_argument(
        '--release_version', default='v1', type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    # basic dataset information
    info = {"year" : 2020,
                "version" : "1.5",
                "description" : "xView-COCO",
                "contributor" : "paulikarl",
                "url" : "paulikarl.cn",
                "date_created" : "2020"
            }
    
    licenses = [{"id": 1,
                    "name": "Attribution-NonCommercial",
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                }]

    # DOTA dataset's information
    image_format='.png'
    anno_format='.txt'
    core_dataset = 'xview'

    original_class = {'Maritime Vessel':1, 'Motorboat':2, 'Sailboat':3, 'Tugboat':4, 'Barge':5, 'Fishing Vessel':6, 'Ferry':7, 'Yacht':8, 'Container Ship':9,'Oil Tanker':10}
    converted_class = [{'supercategory': 'none', 'id': 1,  'name': 'Maritime Vessel', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 2,  'name': 'Motorboat', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 3,  'name': 'Sailboat', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 4,  'name': 'Tugboat', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 5,  'name': 'Barge', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 6,  'name': 'Fishing Vessel', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 7,  'name': 'Ferry', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 8,  'name': 'Yacht', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 9,  'name': 'Container Ship', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
        {'supercategory': 'none', 'id': 10,  'name': 'Oil Tanker', "skeleton": [[1,2], [2,3], [3,4], [4,1]]},
    ]
    imagesets = ['trainval','test']
    release_version = 'v1'
    #/data/pd/xview/v1/
    for imageset in imagesets:
        imgpath = '/data/pd/{}/{}/{}/images'.format(core_dataset, release_version, imageset)
        annopath = '/data/pd/{}/{}/{}/labels'.format(core_dataset, release_version, imageset)
        save_path = '/data/pd/{}/{}/coco/annotations'.format(core_dataset, release_version)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        xView = xView2COCO(imgpath=imgpath,
                        annopath=annopath,
                        image_format=image_format,
                        anno_format=anno_format,
                        data_categories=converted_class,
                        data_info=info,
                        data_licenses=licenses,
                        data_type="instances",
                        groundtruth=True,
                        small_object_area=0)

        images, annotations = xView.get_image_annotation_pairs()

        json_data = {"info" : xView.info,
                    "images" : images,
                    "licenses" : xView.licenses,
                    "type" : xView.type,
                    "annotations" : annotations,
                    "categories" : xView.categories}

        with open(os.path.join(save_path, core_dataset + "_" + imageset + "_" + release_version + ".json"), "w") as jsonfile:
            json.dump(json_data, jsonfile, sort_keys=True, indent=4)