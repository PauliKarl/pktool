import argparse
import os
import cv2
import json
import numpy as np

import mmcv
from pycocotools import mask as maskUtils
from pktool import Convert2COCO, pointobb2bbox, bbox2pointobb, pointobb_best_point_sort, pointobb_extreme_sort, thetaobb2pointobb

class hrsc2COCO(Convert2COCO):
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
            thetaObb = [float(xy) for xy in line.rstrip().split(' ')[:5]]
            
            pointsObb = thetaobb2pointobb(thetaObb)

            gt_label = " ".join(line.rstrip().split(' ')[5:])

            xmin = min(pointsObb[0::2])
            ymin = min(pointsObb[1::2])
            xmax = max(pointsObb[0::2])
            ymax = max(pointsObb[1::2])
            bbox_w = xmax - xmin
            bbox_h = ymax - ymin

            #pointobb = bbox2pointobb([xmin, ymin, xmax, ymax])
            obj_struct['segmentation'] = pointsObb
            obj_struct['pointobb'] = pointobb_sort_function[pointobb_sort_method](pointsObb)
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
            "description" : "HRSC-COCO",
            "contributor" : "paulikarl",
            "url" : "paulikarl.cn",
            "date_created" : "2021"
            }
    
    licenses = [{"id": 1,
                    "name": "Attribution-NonCommercial",
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                }]

    # DOTA dataset's information
    image_format='.bmp'
    anno_format='.txt'
    core_dataset = 'hrsc2016'

    original_class = {'尼米兹级航母':1, 
                    '塔拉瓦级通用两栖攻击舰':2,
                    '提康德罗加级巡洋舰':3,
                    '奥斯汀级两栖船坞运输舰':4,
                    '阿利伯克级驱逐舰':5,
                    '货船(_|.--.--|_]=':6,
                    '船':6,
                    '佩里级护卫舰':7,
                    '运输汽车船(======|':6,
                    '运输汽车船([]==[])':6,
                    '惠德贝岛级船坞登陆舰':8,
                    '圣安东尼奥级两栖船坞运输舰':9,
                    '军舰':6,
                    '中途号航母':1,
                    '琵琶形军舰':6,
                    '尾部OX头部圆指挥舰':10,
                    '气垫船':6,
                    '医疗船':6,
                    '集装箱货船':6,
                    '企业级航母':1,
                    '游轮':6,
                    '小鹰级航母':1,
                    '潜艇':11,
                    '商船':6,
                    '游艇':6,
                    '蓝岭级指挥舰':12,
                    '俄罗斯库兹涅佐夫号航母':1,
                    '航母':1
                    }

    converted_class = [{'supercategory': 'none', 'id': 1,  'name': '航母'},
        {'supercategory': 'none', 'id': 2,  'name': '塔拉瓦级通用两栖攻击舰'},
        {'supercategory': 'none', 'id': 3,  'name': '提康德罗加级巡洋舰'},
        {'supercategory': 'none', 'id': 4,  'name': '奥斯汀级两栖船坞运输舰'},
        {'supercategory': 'none', 'id': 5,  'name': '阿利伯克级驱逐舰'},
        {'supercategory': 'none', 'id': 6,  'name': '船'},
        {'supercategory': 'none', 'id': 7,  'name': '佩里级护卫舰'},
        {'supercategory': 'none', 'id': 8,  'name': '惠德贝岛级船坞登陆舰'},
        {'supercategory': 'none', 'id': 9,  'name': '圣安东尼奥级两栖船坞运输舰'},
        {'supercategory': 'none', 'id': 10,  'name': '指挥舰'},
        {'supercategory': 'none', 'id': 11,  'name': '潜艇'},
        {'supercategory': 'none', 'id': 12,  'name': '蓝岭级指挥舰'}
    ]
    imagesets = ['trainval', 'test']
    release_version = 'v1'

    pointobb_sort_method = 'best' # or "extreme"
    pointobb_sort_function = {"best": pointobb_best_point_sort,
                            "extreme": pointobb_extreme_sort}
    #/data/pd/xview/v1/
    for imageset in imagesets:
        imgpath = '/data/hrsc2016/release/v0/{}/images'.format(imageset)
        annopath = '/data/pd/hrsc2016/v0/{}/annotations'.format(imageset)

        save_path = '/data/pd/{}/{}/coco/annotations'.format(core_dataset, release_version)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        hrsc = hrsc2COCO(imgpath=imgpath,
                        annopath=annopath,
                        image_format=image_format,
                        anno_format=anno_format,
                        data_categories=converted_class,
                        data_info=info,
                        data_licenses=licenses,
                        data_type="instances",
                        groundtruth=True,
                        small_object_area=0)

        images, annotations = hrsc.get_image_annotation_pairs()

        json_data = {"info" : hrsc.info,
                    "images" : images,
                    "licenses" : hrsc.licenses,
                    "type" : hrsc.type,
                    "annotations" : annotations,
                    "categories" : hrsc.categories}

        with open(os.path.join(save_path, core_dataset + "_" + imageset + "_" + release_version + ".json"), "w") as jsonfile:
            json.dump(json_data, jsonfile, sort_keys=True, indent=4)