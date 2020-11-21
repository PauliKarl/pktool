import argparse
import os
import cv2
import json
import numpy as np

import mmcv
from pycocotools import mask as maskUtils
from pktool import Convert2COCO, pointobb2bbox, bbox2pointobb, pointobb_best_point_sort, pointobb_extreme_sort

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
    core_dataset = 'ship'

    original_class = {'船-两栖指挥舰-蓝岭级-蓝岭号':1, '船-航空母舰-尼米兹级-里根号':2, '船-驱逐舰-阿利伯克级-马斯廷号':3, 
                        '船-巡洋舰-提康德罗加级-安提坦号':4, '船-巡洋舰-提康德罗加级-钱斯洛斯维尔号':5, '船-军辅船-NULL-NULL':6, 
                        '船-巡洋舰-提康德罗加级-夏伊洛号':7, '船-驱逐舰-阿利伯克级-巴里号':8, '船-驱逐舰-阿利伯克级-本福德号':9,
                        '船-驱逐舰-阿利伯克级-威尔伯号':10, '船-驱逐舰-阿利伯克级-麦凯恩号':11, '船-驱逐舰-阿利伯克级-斯坦赛姆号':12,
                        '船-驱逐舰-旗风级-旗风号':13, '船-驱逐舰-金刚级-金刚号':14, '船-驱逐舰-朝雾级-天雾号':15, 
                        '船-驱逐舰-秋月级-照月号':16, '船-驱逐舰-高波级-大波号':17, '船-扫雷母舰-浦贺级-浦贺号':18,
                        '船-海洋观测舰--二见级-若狭号':19, '船-潜艇救难舰--NULL-千代田号':20, '船-潜艇-NULL-NULL':21,
                        '船-驱逐舰-阿利伯克级-米利厄斯号':22, '船-两栖指挥舰舰-蓝岭级-蓝领号':23, '船-巡洋舰-提康德罗加级-夏洛伊号':24,
                        '船-巡洋舰-天雾级-海雾号':25, '船-护卫舰-阿武隈级-阿武隈号':26, '船-巡洋舰-金刚级-雾岛号':27,
                        '船-巡洋舰-高波级-高波号':28, '船-两栖登陆舰-海洋之子级-海洋之子号':29, '船-潜艇--NULL-NULL':30,
                        '船-直升机驱逐舰--出云级-出云号':31, '船-驱逐舰-村雨级-村雨号':32, '船-驱逐舰--飞鸟级-飞鸟号':33,
                        '船-海洋观测舰--二见级-日南号':34}
    converted_class = [{'supercategory': 'none', 'id': 1,  'name': '船-两栖指挥舰-蓝岭级-蓝岭号'},
        {'supercategory': 'none', 'id': 2,  'name': '船-航空母舰-尼米兹级-里根号'},
        {'supercategory': 'none', 'id': 3,  'name': '船-驱逐舰-阿利伯克级-马斯廷号'},
        {'supercategory': 'none', 'id': 4,  'name': '船-巡洋舰-提康德罗加级-安提坦号'},
        {'supercategory': 'none', 'id': 5,  'name': '船-巡洋舰-提康德罗加级-钱斯洛斯维尔号'},
        {'supercategory': 'none', 'id': 6,  'name': '船-军辅船-NULL-NULL'},
        {'supercategory': 'none', 'id': 7,  'name': '船-巡洋舰-提康德罗加级-夏伊洛号'},
        {'supercategory': 'none', 'id': 8,  'name': '船-驱逐舰-阿利伯克级-巴里号'},
        {'supercategory': 'none', 'id': 9,  'name': '船-驱逐舰-阿利伯克级-本福德号'},
        {'supercategory': 'none', 'id': 10,  'name': '船-驱逐舰-阿利伯克级-威尔伯号'},
        {'supercategory': 'none', 'id': 11,  'name': '船-驱逐舰-阿利伯克级-麦凯恩号'},
        {'supercategory': 'none', 'id': 12,  'name': '船-驱逐舰-阿利伯克级-斯坦赛姆号'},
        {'supercategory': 'none', 'id': 13,  'name': '船-驱逐舰-旗风级-旗风号'},
        {'supercategory': 'none', 'id': 14,  'name': '船-驱逐舰-金刚级-金刚号'},
        {'supercategory': 'none', 'id': 15,  'name': '船-驱逐舰-朝雾级-天雾号'},
        {'supercategory': 'none', 'id': 16,  'name': '船-驱逐舰-秋月级-照月号'},
        {'supercategory': 'none', 'id': 17,  'name': '船-驱逐舰-高波级-大波号'},
        {'supercategory': 'none', 'id': 18,  'name': '船-扫雷母舰-浦贺级-浦贺号'},
        {'supercategory': 'none', 'id': 19,  'name': '船-海洋观测舰--二见级-若狭号'},
        {'supercategory': 'none', 'id': 20,  'name': '船-潜艇救难舰--NULL-千代田号'},
        {'supercategory': 'none', 'id': 21,  'name': '船-潜艇-NULL-NULL'},
        {'supercategory': 'none', 'id': 22,  'name': '船-驱逐舰-阿利伯克级-米利厄斯号'},
        {'supercategory': 'none', 'id': 23,  'name': '船-两栖指挥舰舰-蓝岭级-蓝领号'},
        {'supercategory': 'none', 'id': 24,  'name': '船-巡洋舰-提康德罗加级-夏洛伊号'},
        {'supercategory': 'none', 'id': 25,  'name': '船-巡洋舰-天雾级-海雾号'},
        {'supercategory': 'none', 'id': 26,  'name': '船-护卫舰-阿武隈级-阿武隈号'},
        {'supercategory': 'none', 'id': 27,  'name': '船-巡洋舰-金刚级-雾岛号'},
        {'supercategory': 'none', 'id': 28,  'name': '船-巡洋舰-高波级-高波号'},
        {'supercategory': 'none', 'id': 29,  'name': '船-两栖登陆舰-海洋之子级-海洋之子号'},
        {'supercategory': 'none', 'id': 30,  'name': '船-潜艇--NULL-NULL'},
        {'supercategory': 'none', 'id': 31,  'name': '船-直升机驱逐舰--出云级-出云号'},
        {'supercategory': 'none', 'id': 32,  'name': '船-驱逐舰-村雨级-村雨号'},
        {'supercategory': 'none', 'id': 33,  'name': '船-驱逐舰--飞鸟级-飞鸟号'},
        {'supercategory': 'none', 'id': 34,  'name': '船-海洋观测舰--二见级-日南号'}
    ]
    imagesets = ['trainval']
    release_version = 'v0'

    pointobb_sort_method = 'best' # or "extreme"
    pointobb_sort_function = {"best": pointobb_best_point_sort,
                            "extreme": pointobb_extreme_sort}
    #/data/pd/xview/v1/
    for imageset in imagesets:
        imgpath = '/home/pd/data/images'
        annopath = '/home/pd/data/labels'

        save_path = '/home/pd/data/{}/{}/coco/annotations'.format(core_dataset, release_version)
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