import numpy as np
import cv2
import os
from pktool import thetaobb2pointobb, mkdir_or_exist
from .color import is_str, color_val

def imshow_bboxes(img_or_path,
                  bboxes,
                  labels=None,
                  scores=None,
                  score_threshold=0.0,
                  colors='red',
                  cls_map=None,
                  show_label=False,
                  show_score=True,
                  thickness=3,
                  show=True,
                  win_name='',
                  wait_time=0,
                  out_file=None,
                  origin_file=None,
                  return_img=False):
    """ Draw horizontal bounding boxes on image

    Args:
        img (str or ndarray): The image to be displayed.
        bboxes (list or ndarray): A ndarray of shape (N, 4)
        labels (list or ndarray): A ndarray of shape (N, 1)
        scores (list or ndarray): A ndarray of shape (N, 1)
    """
    if is_str(img_or_path):
        img = cv2.imread(img_or_path)
        img_origin = img.copy()
    else:
        img = img_or_path
        img_origin = img.copy()

    if len(bboxes) == 0:
        if win_name == '':
            cv2.namedWindow("results", 0)
            win_name = "results"
        cv2.imshow(win_name, img)
        cv2.waitKey(wait_time)
        return

    if isinstance(bboxes, list):
        bboxes = np.array(bboxes)

    if bboxes.ndim == 1:
        bboxes = np.array([bboxes])

    if labels is None:
        labels_vis = np.array(['ins'] * bboxes.shape[0])
    else:
        labels_vis = np.array(labels)
        if labels_vis.ndim == 0:
            labels_vis = np.array([labels_vis])

    if scores is None:
        scores_vis = np.array([1.0] * bboxes.shape[0])
    else:
        scores_vis = np.array(scores)
        if scores_vis.ndim == 0:
            scores_vis = np.array([scores_vis])

    if labels is None:
        colors = dict()
        colors[colors] = color_val(colors)
    else:
        max_label = max(labels)
        colors = [color_val(_) for _ in range(max_label + 1)]

    for bbox, label, score in zip(bboxes, labels_vis, scores_vis):
        if score < score_threshold:
            continue
        bbox = bbox.astype(np.int32)
        xmin, ymin, xmax, ymax = bbox
        if cls_map is None:
            label_str = str(label)
        else:
            label_str = [k for k,v in cls_map.items() if v==label][0]

        current_color = colors[label]
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=current_color, thickness=thickness)

        if show_label:
            cv2.putText(img, label, (xmin, ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale = 1.0, color = current_color, thickness = 2, lineType = 8)
        if show_score:
            cv2.putText(img, "{:.2f}".format(score), (xmin, ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale = 1.0, color = current_color, thickness = 2, lineType = 8)

    if show:
        if win_name == '':
            cv2.namedWindow("results", 0)
            win_name = "results"
        cv2.imshow(win_name, img)
        cv2.waitKey(wait_time)
        cv2.destroyAllWindows()
    if out_file is not None:
        dir_name = os.path.abspath(os.path.dirname(out_file))
        mkdir_or_exist(dir_name)
        cv2.imwrite(out_file, img)
    if origin_file is not None:
        dir_name = os.path.abspath(os.path.dirname(origin_file))
        mkdir_or_exist(dir_name)
        cv2.imwrite(origin_file, img_origin)
    if return_img:
        return img

def imshow_rbboxes(img_or_path,
              rbboxes,
              labels=None,
              scores=None,
              score_threshold=0.0,
              colors='red',
              cls_map=None,
              show_label=False,
              show_score=False,
              thickness=2,
              show=True,
              win_name='',
              wait_time=0,
              out_file=None,
              return_img=False):
    """ Draw oriented bounding boxes on image

    Args:
        img (str or ndarray): The image to be displayed.
        rbboxes (list or ndarray): A ndarray of shape (N, 5) or pointobbs
        cls_map (dict): key=classname val=label
        labels (list or ndarray): A ndarray of shape (N, 1)
        scores (list or ndarray): A ndarray of shape (N, 1)
    """
    if is_str(img_or_path):
        img = cv2.imread(img_or_path)
    else:
        img = img_or_path

    if rbboxes == []:
        return

    if isinstance(rbboxes, list):
        rbboxes = np.array(rbboxes)
    
    if rbboxes.shape[1] == 5:
        rbboxes_ = []
        for rbbox in rbboxes:
            rbboxes_.append(thetaobb2pointobb(rbbox))
        rbboxes = np.array(rbboxes_)
    if rbboxes.ndim == 1:
        rbboxes = np.array([rbboxes])

    if labels is None:
        labels_vis = np.array(['ins'] * rbboxes.shape[0])
    else:
        labels_vis = np.array(labels)
        if labels_vis.ndim == 0:
            labels_vis = np.array([labels_vis])

    if scores is None:
        scores_vis = np.array([1.0] * rbboxes.shape[0])
    else:
        scores_vis = np.array(scores)
        if scores_vis.ndim == 0:
            scores_vis = np.array([scores_vis])
    if cls_map is None:
        cls_map={"ship":1}
    if labels is None:
        colors = dict()
        colors[colors] = color_val(colors)
    else:
        max_label = max(labels)
        colors = [color_val(_) for _ in range(max_label + 1)]

    for rbbox, label, score in zip(rbboxes, labels_vis, scores_vis):
        if score < score_threshold:
            continue
        if len(rbbox) == 5:
            rbbox = np.array(thetaobb2pointobb(rbbox))
        rbbox = rbbox.astype(np.int32)

        cx = int(round(np.mean(rbbox[::2])))
        cy = int(round(np.mean(rbbox[1::2])))

        if cls_map is None:
            label_str = str(label)
        else:
            label_str = [k for k,v in cls_map.items() if v==label][0]
        current_color = colors[label]

        for idx in range(-1, 3, 1):
            cv2.line(img, (int(rbbox[idx*2]), int(rbbox[idx*2+1])), (int(rbbox[(idx+1)*2]), int(rbbox[(idx+1)*2+1])), current_color, thickness=thickness)

        if show_label:
            cv2.putText(img, label_str, (cx, cy-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale = 0.6, color = current_color, thickness = 2, lineType = 8)
        if show_score:
            cv2.putText(img, label_str + "{:.2f}".format(score), (cx, cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale = 1.0, color = current_color, thickness = 1, lineType = 8)

    if show:
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        cv2.imshow(win_name, img)
        cv2.waitKey(wait_time)
        cv2.destroyAllWindows()
    if out_file is not None:
        dir_name = os.path.abspath(os.path.dirname(out_file))
        mkdir_or_exist(dir_name)
        cv2.imwrite(out_file, img)
    if return_img:
        return img