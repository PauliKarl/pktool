import os
import shutil
from pktool import mkdir_or_exist




if __name__=='__main__':

    labelFolder='/data/pd/ext/ship/v1/labels/'
    imageFolder = '/data/pd/ext/ship/v1/images/'

    filtered_image_path = '/data2/pd/sdc/shipdet/ext/v1/trainval/images/'
    filtered_label_path = '/data2/pd/sdc/shipdet/ext/v1/trainval/labels/'
    mkdir_or_exist(filtered_image_path)
    mkdir_or_exist(filtered_label_path)

    for labeltxt in os.listdir(labelFolder):
        labelpath = labelFolder + labeltxt
        shutil.copy(labelpath,filtered_label_path)
        imgpath = imageFolder + labeltxt.split('.txt')[0] + '.png'
        shutil.copy(imgpath,filtered_image_path)
