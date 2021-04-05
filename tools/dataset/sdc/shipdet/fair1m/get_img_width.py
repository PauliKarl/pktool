import os
import cv2
MAX_IMG_LENGTH = 0
MIN_IMG_LENGTH = 500000

png_path = '/data2/pd/sdc/shipdet/fair1m/v0/trainval/images/'



# img_list,_ = get_files(label_path,_ends=["*.txt"])

for idx, imgfile in enumerate(os.listdir(png_path)):
    
    new_file = png_path + imgfile
    print(idx, imgfile)
    if os.path.isfile(new_file):
        img=cv2.imread(new_file)
        h,w = img.shape[0],img.shape[1]
        MAX_IMG_LENGTH = max(MAX_IMG_LENGTH,h,w)
        MIN_IMG_LENGTH = min(MIN_IMG_LENGTH,h,w)
    else:
        print(img_file)
        break


print(MAX_IMG_LENGTH,MIN_IMG_LENGTH)