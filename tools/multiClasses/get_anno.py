import os
import chardet
import codecs
from pktool import mkdir_or_exist, get_files, PascalVocReader
import sys

classes = {}

dir_ = "F:/opticalship/images/19"
xmlList,_ = get_files(dir_,_ends=['*.xml'])

for file_lab in xmlList:
    xmlread = PascalVocReader(file_lab)
    shapes = xmlread.getShapes()
    for label, points, direction, isRotated, difficult in shapes:
        if label in classes:
            classes[label]+=1
        else:
            classes[label]=1

print(classes)
