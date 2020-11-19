## convert annotations(rslabel) to txt
import json
import os
import glob
import numpy as np

from tqdm import tqdm
from pktool import get_files


def get_annotation_from_json(file_path):
    """ convert annotation format(from rslabel tool)

    Args:
        file_path: label file
    return:
        coords: list[float] Nx8
        labels: list[str] Nx1
    """
    with open(file_path,'r', encoding='utf-8') as f:
        ann_dict = json.load(f)
    coords = []
    labels = []
    x0 = ann_dict['geoTrans'][0]
    x_ratio = ann_dict['geoTrans'][1]

    y0 = ann_dict['geoTrans'][3]
    y_ratio = ann_dict['geoTrans'][5]

    for i in range(len(ann_dict['shapes'])):
        points = np.array(ann_dict['shapes'][i]['points']).reshape(8,)
        points[::2] = x_ratio*(points[::2]-x0)
        points[1::2] = y_ratio*(points[1::2]-y0)
        coords.append(points)
        labels.append(ann_dict['shapes'][i]['label'])
    return coords, labels

def dump_txt(txt_path,coords, labels):
    f = open(txt_path,mode='w')
    print(txt_path)
    for i in range(len(labels)):
        points = coords[i]
        label = labels[i]
        f.write(str(points[0])+","+str(points[1])+","+str(points[2])+","+str(points[3])+","+
                str(points[4])+","+str(points[5])+","+str(points[6])+","+str(points[7])+","+label+"\n")

    f.close()
    return

if __name__=='__main__':
    dir_json = 'F:\data\gei_wd'

    file_list, file_num = get_files(dir_json)
    classname = {}
    obj_num = 0
    for fle in file_list:
        coords, labels = get_annotation_from_json(fle)
        obj_num+=len(labels)
        for label in labels:
            if label not in classname:
                classname[label]=1
            else:
                classname[label]+=1
    rdata = dir_json + "/rdata.txt"
    f = open(rdata,mode='w')
    for c in classname:
        f.write(c+","+str(classname[c])+"\n") 
    f.close()
        #txt_path = fle.split('.json')[0] + '.txt'
        #dump_txt(txt_path,coords, labels)
    print(obj_num,len(classname))
        
