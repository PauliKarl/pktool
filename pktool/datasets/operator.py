import os
import shutil
import numpy as np
import pktool
import cv2

def shuffle_dataset(origin_dataset_dir, trainval_dir, test_dir, trainval_rate=0.8, image_format='.png', label_format='.txt', seed=0,is_print=False):
    """Generate trainval and test sets from origin set by copying files randomly.
    
    Arguments:
        origin_dataset_dir {str} -- path of origin dataset, contains `images` and `labels` folds
        trainval_dir {str} -- path of trainval set, contains `images` and `labels` folds
        test_dir {str} -- path of test set, contains `images` and `labels` folds
        seed {int} -- seed of random function
    
    Returns:
        None
    """
    np.random.seed(seed)
    src_label_path = os.path.join(origin_dataset_dir, 'labels')
    src_image_path = os.path.join(origin_dataset_dir, 'images')

    trainval_dst_label_path = os.path.join(trainval_dir, 'labels')
    pktool.mkdir_or_exist(trainval_dst_label_path)
    trainval_dst_image_path = os.path.join(trainval_dir, 'images')
    pktool.mkdir_or_exist(trainval_dst_image_path)

    test_dst_label_path = os.path.join(test_dir, 'labels')
    pktool.mkdir_or_exist(test_dst_label_path)
    test_dst_image_path = os.path.join(test_dir, 'images')
    pktool.mkdir_or_exist(test_dst_image_path)

    file_names = [label_file.split('.txt')[0] for label_file in os.listdir(src_label_path)]
    file_names = sorted(file_names)
    np.random.shuffle(file_names)

    print(len(file_names))
    trainval_file_names = file_names[0 : int(len(file_names) * trainval_rate)]
    test_file_names = file_names[int(len(file_names) * trainval_rate):]

    for trainval_file_name in trainval_file_names:
        if is_print:
            print("From {} to {}.".format(os.path.join(src_label_path, trainval_file_name), os.path.join(trainval_dst_label_path, trainval_file_name)))
        shutil.copy(os.path.join(src_label_path, trainval_file_name + label_format), os.path.join(trainval_dst_label_path, trainval_file_name + label_format))
        shutil.copy(os.path.join(src_image_path, trainval_file_name + image_format), os.path.join(trainval_dst_image_path, trainval_file_name + image_format))

    for test_file_name in test_file_names:
        if is_print:
            print("From {} to {}.".format(os.path.join(src_label_path, test_file_name), os.path.join(test_dst_label_path, test_file_name)))
        shutil.copy(os.path.join(src_label_path, test_file_name + label_format), os.path.join(test_dst_label_path, test_file_name + label_format))
        shutil.copy(os.path.join(src_image_path, test_file_name + image_format), os.path.join(test_dst_image_path, test_file_name + image_format))


def split_image(img, subsize=1024, gap=200, mode='keep_all'):
    img_height, img_width = img.shape[0], img.shape[1]

    start_xs = np.arange(0, img_width-gap, subsize - gap)
    if mode == 'keep_all':
        start_xs[-1] = img_width - subsize if img_width - start_xs[-1] <= subsize else start_xs[-1]
    elif mode == 'drop_boundary':
        if img_width - start_xs[-1] < subsize - gap:
            start_xs = np.delete(start_xs, -1)
    start_xs[-1] = np.maximum(start_xs[-1], 0)

    start_ys = np.arange(0, img_height-gap, subsize - gap)
    if mode == 'keep_all':
        start_ys[-1] = img_height - subsize if img_height - start_ys[-1] <= subsize else start_ys[-1]
    elif mode == 'drop_boundary':
        if img_height - start_ys[-1] < subsize - gap:
            start_ys = np.delete(start_ys, -1)
    start_ys[-1] = np.maximum(start_ys[-1], 0)

    subimages = dict()
    for start_x in start_xs:
        for start_y in start_ys:
            end_x = np.minimum(start_x + subsize, img_width)
            end_y = np.minimum(start_y + subsize, img_height)
            subimage = img[start_y:end_y, start_x:end_x, ...]
            coordinate = (start_x, start_y)
            subimages[coordinate] = subimage
    return subimages

def padding_image(img,pad_top,pad_bottom,pad_left,pad_right,paddingType=cv2.BORDER_CONSTANT,value=0):
    """padding source image
    args:
        img: source image, for example a np.ndarray [height, width, channel]
        pad_x:int,For example, pad_top=1, pad_bottom=1, pad_left=1, pad_right=1 mean that 1 pixel-wide border needs 
        paddingType: padding style. 
            cv2.BORDER_CONSTANT---padding with value
            cv2.BORDER_REFLECT ---e.g. gfedcb|abcdefgh|gfedcba
            cv2.BORDER_REFLECT_101 or cv2.BORDER_DEFAULT---gfedcb|abcdefgh|gfedcba
            cv2.BORDER_REPLICATE---aaaaaa|abcdefgh|hhhhhhh
            cv2.BORDER_WRAP---cdefgh|abcdefgh|abcdefg
        value: if paddingType is cv2.BORDER_CONSTANT, value must be int
    return:
        img: padded images
    """
    if  not isinstance(img,np.ndarray):
        raise TypeError('argument img must be numpy.ndarray')
    
    img = cv2.copyMakeBorder(img,pad_top,pad_bottom,pad_left,pad_right,paddingType,value=value)

    return img