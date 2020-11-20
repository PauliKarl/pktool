from pktool import get_files
import cv2


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

root_path = 'F:\data\gei_wd'
img_list,_ = get_files(root_path,_ends=["*.tiff"])
for idx, img_file in enumerate(img_list):
    print(idx, img_file)
    new_file = img_file.split('.tiff')[0] + '.png'

    img,_ = read_gaofen(img_file)

    cv2.imwrite(new_file, img)

