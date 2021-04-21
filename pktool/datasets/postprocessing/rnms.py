import numpy as np
import cv2

def roRect_nms(rbboxes, scores, iou_threshold=0.5, score_threshold=0.001, soft=False):
    """rotation non-maximum suppression (NMS) on the boxes according to their intersection-over-union (IoU)
    Arguments:
        rboxes {np.array} -- [N * 5] (cx, cy, w, h, theta (rad/s))
        scores {np.array} -- [N * 1]
        iou_threshold {float} -- threshold for IoU
    """
    rbboxes = np.array(rbboxes)
    scores = np.array(scores)
    cx = rbboxes[:, 0]
    cy = rbboxes[:, 1]
    w = rbboxes[:, 2]
    h = rbboxes[:, 3]
    theta = rbboxes[:, 4] * 180.0 / np.pi

    order = scores.argsort()[::-1]

    areas = w * h
    
    keep = []
    while order.size > 0:
        best_rbox_idx = order[0]
        keep.append(best_rbox_idx)

        best_rbbox = np.array([cx[best_rbox_idx], 
                               cy[best_rbox_idx], 
                               w[best_rbox_idx], 
                               h[best_rbox_idx], 
                               theta[best_rbox_idx]])
        remain_rbboxes = np.hstack((cx[order[1:]].reshape(1, -1).T, 
                                    cy[order[1:]].reshape(1,-1).T, 
                                    w[order[1:]].reshape(1,-1).T, 
                                    h[order[1:]].reshape(1,-1).T, 
                                    theta[order[1:]].reshape(1,-1).T))

        inters = []
        for remain_rbbox in remain_rbboxes:
            rbbox1 = ((best_rbbox[0], best_rbbox[1]), (best_rbbox[2], best_rbbox[3]), best_rbbox[4])
            rbbox2 = ((remain_rbbox[0], remain_rbbox[1]), (remain_rbbox[2], remain_rbbox[3]), remain_rbbox[4])
            inter = cv2.rotatedRectangleIntersection(rbbox1, rbbox2)[1]
            if inter is not None:
                inter_pts = cv2.convexHull(inter, returnPoints=True)
                inter = cv2.contourArea(inter_pts)
                inters.append(inter)
            else:
                inters.append(0)

        inters = np.array(inters)

        iou = inters / (areas[best_rbox_idx] + areas[order[1:]] - inters)
        if soft:
            inds = np.where(iou <= iou_threshold)[0]
        else:
            #softNMS
            weights = np.ones(iou.shape) - iou
            scores[order[1:]] = weights * scores[order[1:]]
            inds = np.where(scores[order[1:]] > score_threshold)[0]
        
        order = order[inds + 1]

    return keep