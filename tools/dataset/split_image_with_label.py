import os
import numpy as np
import cv2
from PIL import Image
from skimage.io import imread
from pktool import split_image, mkdir_or_exist, simpletxt_dump, visdrone_parse, pointobb2thetaobb,thetaobb2pointobb, simpletxt_parse, rescale_size,imresize
from pktool import get_files, padding_image, get_key

CLASSES = {'ship':1}
IMG_LENGTH_SDC = 1024
GAP = 200


def split2sdc(origin_label_path,origin_image_path,splited_image_path,splited_label_path):

    label_list,_ = get_files(origin_label_path,_ends=["*.txt"])
    for idx, label_file in enumerate(label_list):
        print(idx, label_file)
        file_name=os.path.split(label_file)[1].split('.txt')[0]
        image_file = origin_image_path+ file_name + '.png'

        # image_file = origin_image_path + "11012"+ '.png'
        img = cv2.imread(image_file)
        height,width = img.shape[0],img.shape[1]

        objects = simpletxt_parse(label_file,space=' ',boxType='points')
        bboxes = np.array([pointobb2thetaobb(obj['points']) for obj in objects]).reshape(-1,5)
        labels = np.array([CLASSES[obj['label']] for obj in objects])

        # if img.shape[-1] != 3:
        #     print(file_name)
        #     continue
        if max(height,width)<IMG_LENGTH_SDC:
            #如果两条边都小于1024，保持比率resize到长边为1024，然后padding短边
            new_size, scale_factor = rescale_size((width, height), (IMG_LENGTH_SDC,IMG_LENGTH_SDC), return_scale=True)
            rescaled_img = imresize(
                img, new_size, interpolation='bilinear', backend='cv2')
            
            bboxes[:,:4] = bboxes[:,:4]*scale_factor
            #padding new_size=(w,h)
            if min(new_size)<IMG_LENGTH_SDC:
                pad_bottom = max(IMG_LENGTH_SDC-new_size[1],0)
                pad_right = max(IMG_LENGTH_SDC-new_size[0],0)
                rescaled_img=padding_image(rescaled_img,0,pad_bottom,0,pad_right,paddingType=cv2.BORDER_CONSTANT,value=0)
            #save img
            image_save_file = splited_image_path + file_name +'.png'
            label_save_file = splited_label_path + file_name +'.txt'
            cv2.imwrite(image_save_file, rescaled_img)
            objects = []
            for i in range(labels.shape[0]):
                subimage_objects = dict()
                subimage_objects['points'] = thetaobb2pointobb(bboxes[i,:])
                subimage_objects['label'] = get_key(CLASSES,labels[i]) 
                objects.append(subimage_objects)
            simpletxt_dump(objects, label_save_file, encode='points')
        else:
            if min(height,width)<IMG_LENGTH_SDC:
                #当有一边小于1024，将小边resize到1024，然后split
                scale_factor = IMG_LENGTH_SDC / min(height,width)
                new_size, scale_factor = rescale_size((width, height), scale_factor, return_scale=True)
                rescaled_img = imresize(
                    img, new_size, interpolation='bilinear', backend='cv2')
                
                bboxes[:,:4] = bboxes[:,:4]*scale_factor
                img = rescaled_img
            #当全部大于1024时，正常分割
            subimages = split_image(img, subsize=IMG_LENGTH_SDC, gap=GAP)
            subimage_coordinates = list(subimages.keys())
            bboxes_ = bboxes.copy()
            labels_ = labels.copy()

            if bboxes_.shape[0] == 0:
                continue

            for subimage_coordinate in subimage_coordinates:

                bboxes_[:, 0] = bboxes[:, 0] - subimage_coordinate[0]
                bboxes_[:, 1] = bboxes[:, 1] - subimage_coordinate[1]
                cx_bool = np.logical_and(bboxes_[:, 0] >= 0, bboxes_[:, 0] < IMG_LENGTH_SDC)
                cy_bool = np.logical_and(bboxes_[:, 1] >= 0, bboxes_[:, 1] < IMG_LENGTH_SDC)
                subimage_bboxes = bboxes_[np.logical_and(cx_bool, cy_bool)]
                subimage_labels = labels_[np.logical_and(cx_bool, cy_bool)]

                if len(subimage_bboxes) == 0:
                    continue
                subimg = subimages[subimage_coordinate]
                if np.mean(img) == 0:
                    continue

                label_save_file = os.path.join(splited_label_path,'{}_{}_{}.txt'.format(file_name, subimage_coordinate[0],subimage_coordinate[1]))
                image_save_file = os.path.join(splited_image_path,'{}_{}_{}.png'.format(file_name, subimage_coordinate[0], subimage_coordinate[1]))
                if min(subimg.shape[:2])<IMG_LENGTH_SDC:
                    print(file_name)
                cv2.imwrite(image_save_file, subimg)

                objects = []
                for subimage_bbox, subimage_label in zip(subimage_bboxes, subimage_labels):
                    subimage_objects = dict()
                    subimage_objects['points'] = thetaobb2pointobb(subimage_bbox.tolist())
                    subimage_objects['label'] = get_key(CLASSES,subimage_label)
                    objects.append(subimage_objects)
                simpletxt_dump(objects, label_save_file,encode='points')
    

def split_all_to_SDC():
    datasets_type = ['dota2.0','hrsc2016','rs']
    datasets=['test','trainval']
    for dataset_type in datasets_type:
        for dataset in datasets:
            origin_label_path = '/data2/pd/sdc/shipdet/{}/v0/{}/labels/'.format(dataset_type,dataset)
            origin_image_path = '/data2/pd/sdc/shipdet/{}/v0/{}/images/'.format(dataset_type,dataset)
            
            if not os.path.exists(origin_label_path):
                print("skipping {}/{}".format(dataset_type,dataset))
                continue
            print("convert and slpiting {}/{}".format(dataset_type,dataset))
            splited_image_path = '/data2/pd/sdc/shipdet/{}/v1/{}/images/'.format(dataset_type,dataset)
            splited_label_path = '/data2/pd/sdc/shipdet/{}/v1/{}/labels/'.format(dataset_type,dataset)
            mkdir_or_exist(splited_image_path)
            mkdir_or_exist(splited_label_path)

            split2sdc(origin_label_path,origin_image_path,splited_image_path,splited_label_path)

def check_size_img():
    flag = True
    datasets_type = ['dota2.0','hrsc2016','rs']
    datasets=['test','trainval']
    for dataset_type in datasets_type:
        for dataset in datasets:
            
            print("checking {}/{}".format(dataset_type,dataset))
            splited_image_path = '/data2/pd/sdc/shipdet/{}/v1/{}/images/'.format(dataset_type,dataset)
            if not os.path.exists(splited_image_path):
                print("skipping{}/{}".format(dataset_type,dataset))
                continue
            for imgName in os.listdir(splited_image_path):
                imgPath = splited_image_path + imgName
                img = cv2.imread(imgPath)
                if img.shape[0]==1024 and img.shape[1]==1024:
                    continue
                print('split failed images:{}'.format(imgPath))
                flag = False
    return flag


if __name__ == '__main__':
    # split_all_to_SDC()
    if check_size_img():
        print("split image ok!")
    else:
        print("something wrong!")