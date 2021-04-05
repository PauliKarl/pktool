from pktool import get_files, mkdir_or_exist
import cv2
import gdal
import os 


def read_gaofen(img_file, convert=None):

    # if img_file is not None:
    data = gdal.Open(img_file)
    #print("finished gdal.Open")
    width = data.RasterXSize
    height = data.RasterYSize


    #高分1三通道图
    band1 = data.GetRasterBand(1)
    img_b = band1.ReadAsArray(0,0,width,height)
    # img_r = (img_r-img_r.min())/(img_r.max()-img_r.min())
    # img_r = np.round(img_r*255)
    # img_r = np.uint8(img_r)

    band2 = data.GetRasterBand(2)
    img_g = band2.ReadAsArray(0,0,width,height)
    # img_g = (img_g-img_g.min())/(img_g.max()-img_g.min())
    # img_g = np.round(img_g*255)
    # img_g = np.uint8(img_g)

    band3 = data.GetRasterBand(3)
    img_r = band3.ReadAsArray(0,0,width,height)
    # img_b = (img_b-img_b.min())/(img_b.max()-img_b.min())
    # img_b = np.round(img_b*255)
    # img_b = np.uint8(img_b)
    img_rgb = cv2.merge([img_r, img_g, img_b])
    img_bgr = cv2.merge([img_b, img_g, img_r])

    return img_rgb, img_bgr

tif_path = '/data2/pd/fair1m/train/part1/images/'
label_path = '/data2/pd/sdc/shipdet/fair1m/v0/trainval/labels'
png_path = '/data2/pd/sdc/shipdet/fair1m/v0/trainval/images/'
mkdir_or_exist(png_path)


# img_list,_ = get_files(label_path,_ends=["*.txt"])

for idx, label_file in enumerate(os.listdir(label_path)):
    
    img_file = tif_path + label_file.split('.txt')[0] + '.tif'
    new_file = png_path + label_file.split('.txt')[0] + '.png'
    print(idx, img_file)
    if os.path.isfile(img_file):
        _, img= read_gaofen(img_file)
        cv2.imwrite(new_file, _)
    else:
        print(img_file)
        break

