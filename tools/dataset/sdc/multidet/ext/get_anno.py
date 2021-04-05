import os
import chardet
import codecs
from pktool import mkdir_or_exist, get_files, PascalVocReader, simpletxt_dump
import sys

def read_classes_ext():

    classes = {}

    dir_ = "/data2/pd/sdc/shipdet/ext/v0/xml/"
    xmlList,_ = get_files(dir_,_ends=['*.xml'])
    print(_)
    for file_lab in xmlList:
        xmlread = PascalVocReader(file_lab)
        shapes = xmlread.getShapes()
        for label, points, direction, isRotated, difficult in shapes:
            if label in classes:
                classes[label]+=1
            else:
                classes[label]=1

    print(classes)

def convert_xml2txt():
    dir_ = "/data2/pd/sdc/shipdet/ext/v0/xml/"
    save_txt = "/data2/pd/sdc/shipdet/ext/v0/origintxt/"
    mkdir_or_exist(save_txt)
    xmlList,_ = get_files(dir_,_ends=['*.xml'])
    print(_)
    for file_lab in xmlList:
        label_save_file = save_txt+os.path.split(file_lab)[-1].split('.xml')[0] + '.txt'

        labels = []
        bboxes = []
        xmlread = PascalVocReader(file_lab)
        shapes = xmlread.getShapes()
        for label, points, direction, _, _ in shapes:
            labels.append(label)
            points_ = []
            for xy in points:
                points_.append(xy[0])
                points_.append(xy[1])
            bboxes.append(points_)

        objects = []
        for bbox, label in zip(bboxes, labels):
            subimage_objects = dict()
            subimage_objects['points'] = bbox
            subimage_objects['label'] = label
            objects.append(subimage_objects)
        simpletxt_dump(objects, label_save_file,encode='points')
        print("save to {}".format(label_save_file))

if __name__=="__main__":
    convert_xml2txt()