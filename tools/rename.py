import os
from pktool import get_files



pngDir = '/data2/pd/sdc/shipdet/v1/coco/annotations/stuffthingmaps/train2017/'

filelist,_ = get_files(pngDir,_ends=['*.png'])

for filename in filelist:
    filename_new = filename.split('.png.png')[0] + '.png'
    os.rename(filename,filename_new)