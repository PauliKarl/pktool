import os
import numpy as np
import cv2
from PIL import Image
from skimage.io import imread
from pktool import split_image, mkdir_or_exist, simpletxt_dump, visdrone_parse, pointobb2thetaobb,thetaobb2pointobb, simpletxt_parse
from pktool import get_files
import gdal

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
            band1 = data.GetRasterBand(3)
            img_r = band1.ReadAsArray(0,0,width,height)
            img_r = (img_r-img_r.min())/(img_r.max()-img_r.min())
            img_r = np.round(img_r*255)
            img_r = np.uint8(img_r)

            band2 = data.GetRasterBand(2)
            img_g = band2.ReadAsArray(0,0,width,height)
            img_g = (img_g-img_g.min())/(img_g.max()-img_g.min())
            img_g = np.round(img_g*255)
            img_g = np.uint8(img_g)

            band3 = data.GetRasterBand(1)
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

Image.MAX_IMAGE_PIXELS = int(2048 * 2048 * 2048 // 4 // 3)

if __name__ == '__main__':

    subimage_size = 1024
    gap = 400

    root_path = 'F:\data\gei_wd'

    image_save_path = 'F:\data\gei_wd\images'
    mkdir_or_exist(image_save_path)
    label_save_path = 'F:\data\gei_wd\labels'
    mkdir_or_exist(label_save_path)

    # print(os.listdir(label_path))
    label_list,_ = get_files(root_path,_ends=["*.txt"])

    for idx, label_file in enumerate(label_list):
        print(idx, label_file)
        file_name=os.path.split(label_file)[1].split('.txt')[0]
        image_file = label_file.split('.txt')[0] + '.tiff'

        img,_ = read_gaofen(image_file)

        objects = simpletxt_parse(label_file,space=',',boxType='points')
        bboxes = np.array([pointobb2thetaobb(obj['points']) for obj in objects])

        labels = np.array([obj['label'] for obj in objects])

        if img.shape[-1] != 3:
            print(file_name)
            continue

        subimages = split_image(img, subsize=subimage_size, gap=gap)
        subimage_coordinates = list(subimages.keys())
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
            img = subimages[subimage_coordinate]
            if np.mean(img) == 0:
                continue

            label_save_file = os.path.join(label_save_path,'{}__{}_{}.txt'.format(file_name, subimage_coordinate[0],subimage_coordinate[1]))
            image_save_file = os.path.join(image_save_path,'{}__{}_{}.png'.format(file_name, subimage_coordinate[0], subimage_coordinate[1]))
            cv2.imwrite(image_save_file, img)

            for subimage_bbox, subimage_label in zip(subimage_bboxes, subimage_labels):
                subimage_objects = dict()
                subimage_objects['points'] = thetaobb2pointobb(subimage_bbox.tolist())
                subimage_objects['label'] = subimage_label
                objects.append(subimage_objects)
            simpletxt_dump(objects, label_save_file,encode='points')