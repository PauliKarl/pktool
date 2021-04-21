import cv2
import os
import numpy as np
from pktool import thetaobb2pointobb, pointobb2thetaobb, rotate_pointobb, simpletxt_dump

def imrotate(img,
             angle,
             center=None,
             scale=1.0,
             border_value=0,
             auto_bound=False):
    """Rotate an image.

    Args:
        img (ndarray): Image to be rotated.
        angle (float): Rotation angle in degrees, positive values mean
            clockwise rotation.
        center (tuple): Center of the rotation in the source image, by default
            it is the center of the image.
        scale (float): Isotropic scale factor.
        border_value (int): Border value.
        auto_bound (bool): Whether to adjust the image size to cover the whole
            rotated image.

    Returns:
        ndarray: The rotated image.
    """
    if center is not None and auto_bound:
        raise ValueError('`auto_bound` conflicts with `center`')
    h, w = img.shape[:2]
    if center is None:
        center = ((w - 1) * 0.5, (h - 1) * 0.5)
    assert isinstance(center, tuple)

    matrix = cv2.getRotationMatrix2D(center, -angle, scale)
    if auto_bound:
        cos = np.abs(matrix[0, 0])
        sin = np.abs(matrix[0, 1])
        new_w = h * sin + w * cos
        new_h = h * cos + w * sin
        matrix[0, 2] += (new_w - w) * 0.5
        matrix[1, 2] += (new_h - h) * 0.5
        w = int(np.round(new_w))
        h = int(np.round(new_h))
    rotated = cv2.warpAffine(img, matrix, (w, h), borderValue=border_value)
    return rotated


def rotation(img,
             thetaobbs,
             labels,
             rotation_angle=45):
    
    #thetaobbs = [[400, 400, 300, 150, 45*np.pi/180], 
    #            [600, 600, 300, 200, 135*np.pi/180]]
    if len(thetaobbs[0])==8:
        pointobbs=thetaobbs
    else:
        pointobbs = [thetaobb2pointobb(thetaobb) for thetaobb in thetaobbs]

    #img = generate_image(1024, 1024)
    img_origin = img.copy()
    #imshow_rbboxes(img, thetaobbs, win_name='origin')

    rotation_angle = rotation_angle
    rotation_anchor = [img.shape[0]//2, img.shape[1]//2]
    
    rotated_img = imrotate(img_origin, rotation_angle)

    rotated_pointobbs = [rotate_pointobb(pointobb, rotation_angle*np.pi/180, rotation_anchor) for pointobb in pointobbs]

    rotated_thetaobbs = [pointobb2thetaobb(rotated_pointobb) for rotated_pointobb in rotated_pointobbs]

    rotated_thetaobbs_ = np.array([obb for obb in rotated_thetaobbs])

    cx_bool = np.logical_and(rotated_thetaobbs_[:, 0] >= 0, rotated_thetaobbs_[:, 0] < 1024)
    cy_bool = np.logical_and(rotated_thetaobbs_[:, 1] >= 0, rotated_thetaobbs_[:, 1] < 1024)

    rotation_thetaobbs = rotated_thetaobbs_[np.logical_and(cx_bool, cy_bool)]
    mm = np.logical_and(cx_bool, cy_bool)
    rotation_labels = []
    for idx, flag in enumerate(mm):
        if flag:
            rotation_labels.append(labels[idx])

    #imshow_rbboxes(rotated_img, rotated_thetaobbs, win_name='rotated')
    bb = rotation_thetaobbs.tolist()
    return rotated_img, bb, rotation_labels


def txt_parse(label_file):
    """parse visdrone style dataset label file

    Arguments:
        label_file {str} -- label file path
        (<bbox_left>, <bbox_top>, <bbox_width>, <bbox_height>, <score>, <object_category>, <truncation>, <occlusion>)

    Returns:
        dict, {'bbox': [xmin, ymin, xmax, ymax], 'label': class_name} -- objects' location and class
    """
    with open(label_file, 'r') as f:
        lines = f.readlines()

    objects = []
    thetaobbes = []
    labels = []
    for line in lines:
        object_struct = dict()
        line = line.rstrip().split(' ')
        label = line[8]
        points = [float(_) for _ in line[0:8]]
        thetaobbes.append(points)
        labels.append(label)

    return thetaobbes, labels

def rotation_main(image_path, label_path, label_list, rotation_angle=45):
    for idx, label_file in enumerate(label_list):
        print(idx, label_file)
        file_name = label_file.split('.txt')[0]
        label_file = os.path.join(label_path, file_name + '.txt')
        image_file = os.path.join(image_path, file_name + '.png')

        img = cv2.imread(image_file)
        
        thetaobbes, labels = txt_parse(label_file)
        #
        img_rotation, thetaobbes_rotation, labels_rotation = rotation(img, thetaobbes, labels,rotation_angle=rotation_angle)

        if len(thetaobbes_rotation)>0:
            objects = []

            for i, thetaobb in enumerate(thetaobbes_rotation):
                single_object = dict()
                single_object["label"] = labels[i]
                single_object['points'] = thetaobb2pointobb(thetaobb)
                objects.append(single_object)

            filename = '{}_ro{}'.format(file_name, rotation_angle)
            label_save_file = label_path + "/" + filename + ".txt"
            image_save_file = image_path + "/" + filename + ".png"
            cv2.imwrite(image_save_file, img_rotation)
            simpletxt_dump(objects, label_save_file,encode='points')

def mixup(img1,img2,lambd):
    ##img1.shape = img2.shape

    height, width=img1.shape[:2]
    mix_img = np.zeros(shape=(height, width, 3), dtype='float32')
    mix_img[:image.shape[0], :image.shape[1], :] = image.astype('float32') * lambd
    mix_img[:image2.shape[0], :image2.shape[1], :] += image2.astype('float32') * (1. - lambd)
    mix_img = mix_img.astype(np.uint8)

    return mix_img

if __name__== '__main__':

    image_path='/home/pd/data/images/'
    label_path='/home/pd/data/labels/'

    # label_list=os.listdir(label_path)

    # rotation_main(image_path, label_path, label_list, rotation_angle=5)
    # #rotation_main(image_path, label_path, label_list, rotation_angle=60)
    # #rotation_main(image_path, label_path, label_list, rotation_angle=90)
    # #rotation_main(image_path, label_path, label_list, rotation_angle=120)
    # #rotation_main(image_path, label_path, label_list, rotation_angle=150)