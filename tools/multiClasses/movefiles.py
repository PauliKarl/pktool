from pktool import get_files, mkdir_or_exist
import os
import shutil

a_dir = 'F:/opticalship/google/'
imageDir = 'F:/opticalship/images/'

imgList = os.listdir(a_dir)

levelset = ['18','19']

mkdir_or_exist(imageDir)

for imgInfo in imgList:

    for level in levelset:

        img,_ = get_files(os.path.join(a_dir,imgInfo,level),_ends=['*.tif'])

        shutil.copy(img[0],os.path.join(imageDir,level))
        print(img[0])