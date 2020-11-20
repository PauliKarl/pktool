from pktool import read_gaofen, get_files
import cv2

root_path = 'F:\data\gei_wd'
img_list,_ = get_files(root_path,_ends=["*.tiff"])
for idx, img_file in enumerate(img_list):
    print(idx, img_file)
    new_file = img_file.split('.tiff')[0] + '.png'

    img,_ = read_gaofen(img_file)

    cv2.imwrite(new_file, img)

