import numpy as np
import cv2

def xyxy2cxcywh(bbox):
    """convert box format [xmin, ymin, xmax, ymax] to [cx, cy, w, h]

    """
    xmin, ymin, xmax, ymax = bbox
    cx = (xmin + xmax) // 2
    cy = (ymin + ymax) // 2
    w = xmax - xmin
    h = ymax - ymin
    
    return [cx, cy, w, h]

def cxcywh2xyxy(bbox):
    """convert box format [cx, cy, w, h] to [xmin, ymin, xmax, ymax]

    """
    cx, cy, w, h = bbox
    xmin = int(cx - w / 2.0)
    ymin = int(cy - h / 2.0)
    xmax = int(cx + w / 2.0)
    ymax = int(cy + h / 2.0)
    
    return [xmin, ymin, xmax, ymax]



def pointobb2thetaobb(pointobb):
    """convert pointobb to thetaobb
    Input:
        pointobb (list[1x8]): [x1, y1, x2, y2, x3, y3, x4, y4]
    Output:
        thetaobb (list[1x5]):[cx, cy, w, h, theta]
    """
    pointobb = np.int0(np.array(pointobb))
    pointobb.resize(4, 2)
    rect = cv2.minAreaRect(pointobb)
    x, y, w, h, theta = rect[0][0], rect[0][1], rect[1][0], rect[1][1], rect[2]
    theta = theta / 180.0 * np.pi
    thetaobb = [x, y, w, h, theta]
    
    return thetaobb

def thetaobb2pointobb(thetaobb):
    """convert thetaobb to pointobb
    Input:
        thetaobb (list[1x5]):[cx, cy, w, h, theta]
    Output:
        thetaobb: (list[1x8]):[x1, y1, x2, y2, x3, y3, x4, y4]
    """
    box = cv2.boxPoints(((thetaobb[0], thetaobb[1]), (thetaobb[2], thetaobb[3]), thetaobb[4] * 180.0 / np.pi))
    box = np.reshape(box, [-1, ]).tolist()
    pointobb = [box[0], box[1], box[2], box[3], box[4], box[5], box[6], box[7]]

    return pointobb

def pointobb2bbox(pointobb):
    """
    docstring here
        :param self: 
        :param pointobb: list, [x1, y1, x2, y2, x3, y3, x4, y4]
        return [xmin, ymin, xmax, ymax]
    """
    xmin = min(pointobb[0::2])
    ymin = min(pointobb[1::2])
    xmax = max(pointobb[0::2])
    ymax = max(pointobb[1::2])
    bbox = [xmin, ymin, xmax, ymax]
    
    return bbox

def bbox2pointobb(bbox):
    """
    docstring here
        :param self: 
        :param bbox: list, [xmin, ymin, xmax, ymax]
        return [x1, y1, x2, y2, x3, y3, x4, y4]
    """
    xmin, ymin, xmax, ymax = bbox
    x1, y1 = xmin, ymin
    x2, y2 = xmax, ymin
    x3, y3 = xmax, ymax
    x4, y4 = xmin, ymax

    pointobb = [x1, y1, x2, y2, x3, y3, x4, y4]
    
    return pointobb


def pointobb_extreme_sort(pointobb):
    """
    Find the "top" point and sort all points as the "top right bottom left" order
        :param self: self
        :param points: unsorted points, (N*8) 
    """   
    points_np = np.array(pointobb)
    points_np.resize(4, 2)
    # sort by Y
    sorted_index = np.argsort(points_np[:, 1])
    points_sorted = points_np[sorted_index, :]
    if points_sorted[0, 1] == points_sorted[1, 1]:
        if points_sorted[0, 0] < points_sorted[1, 0]:
            sorted_top_idx = 0
        else:
            sorted_top_idx = 1
    else:
        sorted_top_idx = 0

    top_idx = sorted_index[sorted_top_idx]
    pointobb = pointobb[2*top_idx:] + pointobb[:2*top_idx]
    
    return pointobb

def pointobb_best_point_sort(pointobb):
    """
    Find the "best" point and sort all points as the order that best point is first point
        :param self: self
        :param points: unsorted points, (N*8) 
    """
    xmin, ymin, xmax, ymax = pointobb2bbox(pointobb)
    w = xmax - xmin
    h = ymax - ymin
    reference_bbox = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
    reference_bbox = np.array(reference_bbox)
    normalize = np.array([1.0, 1.0] * 4)
    combinate = [np.roll(pointobb, 0), np.roll(pointobb, 2), np.roll(pointobb, 4), np.roll(pointobb, 6)]
    distances = np.array([np.sum(((coord - reference_bbox) / normalize)**2) for coord in combinate])
    sorted = distances.argsort()

    return combinate[sorted[0]].tolist()