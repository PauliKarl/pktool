import argparse
import os
import cv2
import json
import numpy as np

import mmcv
from pycocotools import mask as maskUtils
from pktool import Convert2COCO, pointobb2bbox, bbox2pointobb, pointobb_best_point_sort, pointobb_extreme_sort

class SDC2COCO(Convert2COCO):
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
            coco_annotation={}
            bbox = object_struct['bbox']
            label = object_struct['label']

            width = bbox[2]
            height = bbox[3]
            area = height * width

            if area <= self.small_object_area and self.groundtruth:
                self.small_object_idx += 1
                continue

            coco_annotation['segmentation']=[object_struct['segmentation']]
            coco_annotation['bbox'] = bbox
            coco_annotation['category_id'] = label
            coco_annotation['area'] = np.float(area)
            coco_annotation['iscrowd'] = 0
            coco_annotation['num_keypoints'] = 4

            coco_annotations.append(coco_annotation)
            
        return coco_annotations
    
    def __simpletxt_parse__(self, label_file):

        objects = []

        with open(label_file, 'r') as f:
            lines = f.readlines()
        #lines = open(label_file, 'r').readlines()
        for line in lines:
            
            obj_struct = {}
            points = [float(xy) for xy in line.rstrip().split(' ')[:8]]
            
            gt_label = " ".join(line.rstrip().split(' ')[8:])

            xmin = min(points[0::2])
            ymin = min(points[1::2])
            xmax = max(points[0::2])
            ymax = max(points[1::2])
            bbox_w = xmax - xmin
            bbox_h = ymax - ymin

            #pointobb = bbox2pointobb([xmin, ymin, xmax, ymax])
            obj_struct['segmentation'] = points
            obj_struct['pointobb'] = pointobb_sort_function[pointobb_sort_method](points)
            obj_struct['bbox'] = [xmin, ymin, bbox_w, bbox_h]
            obj_struct['label'] = original_class[gt_label]

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
    #args = parse_args()

    # basic dataset information
    info = {"year" : 2021,
            "version" : "1.0",
            "description" : "SDC-multi-COCO",
            "contributor" : "paulikarl",
            "url" : "paulikarl.cn",
            "date_created" : "2021"
            }
    
    licenses = [{"id": 1,
                    "name": "Attribution-NonCommercial",
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                }]

    # DOTA dataset's information
    image_format='.png'
    anno_format='.txt'
    core_dataset = 'sdc'

    original_class = {'Cargo vessel':1,'Ship':2,'Motorboat':3,'Fishing boat':4,'Destroyer':5,'Tugboat':6,'Loose pulley':7,'Warship':8,'Engineering ship':9,'Amphibious ship':10,'Cruiser':11,'Frigate':12,'Submarine':13,'Aircraft carrier':14,'Hovercraft':15,'Command ship':16}
    converted_class = [{'supercategory': 'none', 'id': 1,  'name': 'Cargo vessel'},
                        {'supercategory': 'none', 'id': 2,  'name': 'Ship'},
                        {'supercategory': 'none', 'id': 3,  'name': 'Motorboat'},
                        {'supercategory': 'none', 'id': 4,  'name': 'Fishing boat'},
                        {'supercategory': 'none', 'id': 5,  'name': 'Destroyer'},
                        {'supercategory': 'none', 'id': 6,  'name': 'Tugboat'},
                        {'supercategory': 'none', 'id': 7,  'name': 'Loose pulley'},
                        {'supercategory': 'none', 'id': 8,  'name': 'Warship'},
                        {'supercategory': 'none', 'id': 9,  'name': 'Engineering ship'},
                        {'supercategory': 'none', 'id': 10,  'name': 'Amphibious ship'},
                        {'supercategory': 'none', 'id': 11,  'name': 'Cruiser'},
                        {'supercategory': 'none', 'id': 12,  'name': 'Frigate'},
                        {'supercategory': 'none', 'id': 13,  'name': 'Submarine'},
                        {'supercategory': 'none', 'id': 14,  'name': 'Aircraft carrier'},
                        {'supercategory': 'none', 'id': 15,  'name': 'Hovercraft'},
                        {'supercategory': 'none', 'id': 16,  'name': 'Command ship'}
    ]
    
    imagesets = ['test','trainval']
    release_version = 'v0'

    pointobb_sort_method = 'best' # or "extreme"
    pointobb_sort_function = {"best": pointobb_best_point_sort,
                            "extreme": pointobb_extreme_sort}
    #/data/pd/xview/v1/
    for imageset in imagesets:
        imgpath = '/data2/pd/sdc/multidet/v0/{}/images'.format(imageset)
        annopath = '/data2/pd/sdc/multidet/v0/{}/labels'.format(imageset)

        save_path = '/data2/pd/{}/multidet/{}/coco/annotations'.format(core_dataset, release_version)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        sdc = SDC2COCO(imgpath=imgpath,
                        annopath=annopath,
                        image_format=image_format,
                        anno_format=anno_format,
                        data_categories=converted_class,
                        data_info=info,
                        data_licenses=licenses,
                        data_type="instances",
                        groundtruth=True,
                        small_object_area=0)

        images, annotations = sdc.get_image_annotation_pairs()

        json_data = {"info" : sdc.info,
                    "images" : images,
                    "licenses" : sdc.licenses,
                    "type" : sdc.type,
                    "annotations" : annotations,
                    "categories" : sdc.categories}

        with open(os.path.join(save_path, core_dataset + "_" + imageset + "_" + release_version + ".json"), "w") as jsonfile:
            json.dump(json_data, jsonfile, sort_keys=True, indent=4)