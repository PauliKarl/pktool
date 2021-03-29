from pktool import get_files

img_or_label = 'labels'

datasetPath = '/data2/pd/sdc/multidet/hrsc2016/v0/test/{}/'.format(img_or_label)
#'/data/dota/origin/train/labelTxt-v1.0/'
# dota2.0,
endwith = {'images':['*.png'],'labels':['*.txt'],}
filelist,num = get_files(datasetPath,_ends=endwith[img_or_label])

print(num)

# ###统计图像宽度范围
# import cv2

# MAX_LENGTH = 0
# MIN_LENGTH = 2000000

# for filename in filelist:
#     img = cv2.imread(filename)
#     height, width = img.shape[0],img.shape[1]
#     MAX_LENGTH = max(MAX_LENGTH,height, width)
#     MIN_LENGTH = min(MIN_LENGTH,height, width)

# print(MAX_LENGTH,MIN_LENGTH)