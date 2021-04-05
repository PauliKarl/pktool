import os
import shutil
from pktool import mkdir_or_exist




if __name__=='__main__':

    labelFolder='/data2/pd/sdc/multidet/ext/v0/trainval/labels/'
    imageFolder = '/data2/pd/sdc/shipdet/ext/v0/images/'

    filtered_image_path = '/data2/pd/sdc/multidet/ext/v0/trainval/images/'
    mkdir_or_exist(filtered_image_path)

    for labeltxt in os.listdir(labelFolder):
        imgpath = imageFolder + labeltxt.split('.txt')[0] + '.png'
        shutil.copy(imgpath,filtered_image_path)
