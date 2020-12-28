import os
import argparse
from pktool import split_image, mkdir_or_exist, PascalVocReader, simpletxt_dump, get_files
from pktool import pointobb2thetaobb, split_image, thetaobb2pointobb, get_key

import gdal
import numpy as np
import cv2


def read_gaofen(img_file, convert=None):
    # 返回的图像uint8类型，[r,g,b]
    '''
    if imgFormat == "png" or imgFormat=="jpg":
        img_bgr = cv2.imread(img_file)
        [img_b, img_g, img_r] = cv2.split(img_bgr)
        img_rgb = cv2.merge([img_r, img_g, img_b])
        img_bgr = cv2.merge([img_b, img_g, img_r])
    elif imgFormat == "tif" or imgFormat=="tiff":
    '''
    if img_file is not None:
        data = gdal.Open(img_file)
        #print("finished gdal.Open")
        width = data.RasterXSize
        height = data.RasterYSize

        if data.RasterCount==4:
            #高分2多光谱，4bands，[b,g,r,Nr]
            band1 = data.GetRasterBand(1)
            img_r = band1.ReadAsArray(0,0,width,height)
            img_r = (img_r-img_r.min())/(img_r.max()-img_r.min())
            img_r = np.round(img_r*255)
            img_r = np.uint8(img_r)

            band2 = data.GetRasterBand(2)
            img_g = band2.ReadAsArray(0,0,width,height)
            img_g = (img_g-img_g.min())/(img_g.max()-img_g.min())
            img_g = np.round(img_g*255)
            img_g = np.uint8(img_g)

            band3 = data.GetRasterBand(3)
            img_b = band3.ReadAsArray(0,0,width,height)
            img_b = (img_b-img_b.min())/(img_b.max()-img_b.min())
            img_b = np.round(img_b*255)
            img_b = np.uint8(img_b)
            img_rgb = cv2.merge([img_r, img_g, img_b])
            img_bgr = cv2.merge([img_b, img_g, img_r])

        elif data.RasterCount==3:
            #高分1三通道图
            band1 = data.GetRasterBand(1)
            img_r = band1.ReadAsArray(0,0,width,height)
            img_r = (img_r-img_r.min())/(img_r.max()-img_r.min())
            img_r = np.round(img_r*255)
            img_r = np.uint8(img_r)

            band2 = data.GetRasterBand(2)
            img_g = band2.ReadAsArray(0,0,width,height)
            img_g = (img_g-img_g.min())/(img_g.max()-img_g.min())
            img_g = np.round(img_g*255)
            img_g = np.uint8(img_g)

            band3 = data.GetRasterBand(3)
            img_b = band3.ReadAsArray(0,0,width,height)
            img_b = (img_b-img_b.min())/(img_b.max()-img_b.min())
            img_b = np.round(img_b*255)
            img_b = np.uint8(img_b)
            img_rgb = cv2.merge([img_r, img_g, img_b])
            img_bgr = cv2.merge([img_b, img_g, img_r])

        elif data.RasterCount == 1:
            band1 = data.GetRasterBand(1)
            img_arr = band1.ReadAsArray(0,0,width,height)
            if convert:
                img_mean = img_arr.mean()
                img_sigm = np.sqrt(img_arr.var())
                img_arr[img_arr[:]>img_mean+3*img_sigm]=img_mean+3*img_sigm

            img_arr = (img_arr-img_arr.min())/(img_arr.max()-img_arr.min())
            
            img_arr = np.uint8(np.round(img_arr*255))

            img_rgb = cv2.merge([img_arr,img_arr,img_arr])
            img_bgr = cv2.merge([img_arr,img_arr,img_arr])
    else:
        #raise TypeError("Please input correct image format: png, jpg, tif/tiff!")
        img_rgb = None
        img_bgr = None
    return img_rgb, img_bgr

def parse_args():
    parser = argparse.ArgumentParser(description='split tiff images with labels')
    parser.add_argument('--imageDir', default=None, help='tiff images path')
    parser.add_argument('--labelDir', default=None, help='voc format annotation path')
    parser.add_argument('--saveDir', default=None, help='select path to save images and acc annotations')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    if args.imageDir is not None:
        imageDir = args.imageDir
    else:
        imageDir = 'F:/opticalship/images/18'
    if args.labelDir is not None:
        labelDir = args.labelDir
    else:
        labelDir = 'F:/opticalship/images/18'
    if args.saveDir is not None:
        saveDir = args.saveDir
    else:
        saveDir = 'F:/opticalship/dataset/18'
    
    mkdir_or_exist(saveDir)

    label_save_path = os.path.join(saveDir,'txtlabels')
    mkdir_or_exist(label_save_path)
    image_save_path = os.path.join(saveDir, 'images')
    mkdir_or_exist(image_save_path)


    labelList, _ = get_files(labelDir,_ends=['*.xml'])

    subimage_size = 1024
    gap = 400

    for label_file in labelList:
        basename = os.path.basename(label_file)
        filename, fmt = os.path.splitext(basename)

        _, image = read_gaofen(os.path.join(imageDir,filename+'.tif'))

        reader = PascalVocReader(label_file)

        shapes = reader.getShapes()
        bboxes = []
        labels = []

        tmp_classname = {}
        class_id = 0
        for label, points, direction, _, _ in shapes:
            if label not in tmp_classname:

                tmp_classname[label] = class_id
                label = class_id
                class_id+=1
            else:
                label = tmp_classname[label]
            
            labels.append(label)
            points_ = []
            for xy in points:
                points_.append(xy[0])
                points_.append(xy[1])
            bboxes.append(pointobb2thetaobb(points_))

        subImages = split_image(image,subimage_size,gap)
        subimage_coordinates = list(subImages.keys())
        bboxes = np.array(bboxes)
        labels = np.array(labels)
        bboxes_ = bboxes.copy()
        labels_ = labels.copy()

        if bboxes_.shape[0] == 0:
            continue

        for subimage_coordinate in subimage_coordinates:
            objects = []

            bboxes_[:, 0] = bboxes[:, 0] - subimage_coordinate[0]
            bboxes_[:, 1] = bboxes[:, 1] - subimage_coordinate[1]
            cx_bool = np.logical_and(bboxes_[:, 0] >= 0, bboxes_[:, 0] < subimage_size)
            cy_bool = np.logical_and(bboxes_[:, 1] >= 0, bboxes_[:, 1] < subimage_size)
            subimage_bboxes = bboxes_[np.logical_and(cx_bool, cy_bool)]
            subimage_labels = labels_[np.logical_and(cx_bool, cy_bool)]

            if len(subimage_bboxes) == 0:
                continue
            img = subImages[subimage_coordinate]
            if np.mean(img) == 0:
                continue

            label_save_file = os.path.join(label_save_path,'{}__{}_{}.txt'.format(filename, subimage_coordinate[0],subimage_coordinate[1]))
            image_save_file = os.path.join(image_save_path,'{}__{}_{}.png'.format(filename, subimage_coordinate[0], subimage_coordinate[1]))
            #cv2.imwrite(image_save_file, img)
            cv2.imencode('.png', img)[1].tofile(image_save_file)

            for subimage_bbox, subimage_label in zip(subimage_bboxes, subimage_labels):
                subimage_objects = dict()
                subimage_objects['points'] = thetaobb2pointobb(subimage_bbox.tolist())
                subimage_objects['label'] = get_key(tmp_classname,subimage_label)
                objects.append(subimage_objects)
            simpletxt_dump(objects, label_save_file,encode='points')
    



if __name__ == "__main__":
    main()    
