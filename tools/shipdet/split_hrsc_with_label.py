import os
import numpy as np
import cv2
from pktool import split_image, mkdir_or_exist, simpletxt_dump, visdrone_parse, pointobb2thetaobb,thetaobb2pointobb, simpletxt_parse
from pktool import get_files


imgFormat = '.bmp'
datasets = ['test','trainval']

if __name__ == '__main__':

    subimage_size = 1024

    gap = 200

    for dataset in datasets:

        filtered_label_path = '/data/pd/hrsc2016/ship/v0/{}/annotations/'.format(dataset)

        image_path =  '/data/pd/hrsc2016/ship/v0/{}/images/'.format(dataset)
        
        image_save_path = '/data/pd/hrsc2016/ship/v1/images'
        mkdir_or_exist(image_save_path)
        label_save_path = '/data/pd/hrsc2016/ship/v1/labels'
        mkdir_or_exist(label_save_path)

        # print(os.listdir(label_path))
        label_list,_ = get_files(filtered_label_path,_ends=["*.txt"])

        for idx, label_file in enumerate(label_list):
            print(idx, label_file)
            file_name=os.path.split(label_file)[1].split('.txt')[0]
            image_file = image_path + file_name + imgFormat

            img = cv2.imread(image_file)

            objects = simpletxt_parse(label_file,space=' ',boxType='thetaobb')

            bboxes = np.array([obj['thetaobb'] for obj in objects])

            labels = [obj['label'] for obj in objects]

            if img.shape[-1] != 3:
                print(file_name)
                continue

            subimages = split_image(img, subsize=subimage_size, gap=gap)
            subimage_coordinates = list(subimages.keys())
            bboxes_ = bboxes.copy()
            #labels_ = labels.copy()

            if bboxes_.shape[0] == 0:
                continue

            for subimage_coordinate in subimage_coordinates:
                objects = []

                bboxes_[:, 0] = bboxes[:, 0] - subimage_coordinate[0]
                bboxes_[:, 1] = bboxes[:, 1] - subimage_coordinate[1]
                cx_bool = np.logical_and(bboxes_[:, 0] >= 0, bboxes_[:, 0] < subimage_size)
                cy_bool = np.logical_and(bboxes_[:, 1] >= 0, bboxes_[:, 1] < subimage_size)
                subimage_bboxes = bboxes_[np.logical_and(cx_bool, cy_bool)]

                # subimage_labels = labels_[np.logical_and(cx_bool, cy_bool)]
                # selectLabe=np.logical_and(cx_bool, cy_bool)

                if len(subimage_bboxes) == 0:
                    continue
                img = subimages[subimage_coordinate]
                if np.mean(img) == 0:
                    continue

                label_save_file = os.path.join(label_save_path,'{}__{}_{}.txt'.format(file_name, subimage_coordinate[0],subimage_coordinate[1]))
                image_save_file = os.path.join(image_save_path,'{}__{}_{}.png'.format(file_name, subimage_coordinate[0], subimage_coordinate[1]))
                cv2.imwrite(image_save_file, img)

                for subimage_bbox in subimage_bboxes:
                    subimage_objects = dict()
                    subimage_objects['points'] = thetaobb2pointobb(subimage_bbox.tolist())
                    subimage_objects['label'] = 'ship'
                    objects.append(subimage_objects)
                simpletxt_dump(objects, label_save_file,encode='points')