import pktool
from pktool import get_files,mkdir_or_exist
import os
import cv2

datasets=['test','trainval']


for dataset in datasets:

    label_path = '/data2/pd/sdc/shipdet/hrsc2016/v0/{}/labels/'.format(dataset)
    origin_img_path = '/data/hrsc2016/release/v0/{}/images/'.format(dataset)

    Target_img_path = '/data2/pd/sdc/shipdet/hrsc2016/v0/{}/images/'.format(dataset)
    mkdir_or_exist(Target_img_path)
    for labelfile in os.listdir(label_path):
        OriImgName = labelfile.split('.txt')[0]+'.bmp'
        TarImgName = labelfile.split('.txt')[0]+'.png'


        img = cv2.imread(os.path.join(origin_img_path, OriImgName))

        print("Save image file: ", TarImgName)
        cv2.imwrite(os.path.join(Target_img_path, TarImgName), img)