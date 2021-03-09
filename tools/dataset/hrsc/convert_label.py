from pktool import HRSCReaderCls, get_files, simpletxt_dump, mkdir_or_exist
import os

xmlFolder = '/data/hrsc2016/release/v0/test/annotations/'
saveTxt = '/data/pd/hrsc2016/v0/test/annotations/'
mkdir_or_exist(saveTxt)

clsPath='/home/pd/code/pktool/tools/dataset/hrsc/sysdata.xml'

clsReader = HRSCReaderCls(clsPath=clsPath, layer=1)

clsDict = clsReader.getclsDict()
print(clsDict)

xmlList,_=get_files(xmlFolder,_ends=['*.xml'])

for xmlfile in xmlList:
    basename = os.path.basename(xmlfile)
    filename, fmt = os.path.splitext(basename)

    shapes = clsReader.parseXML(xmlfile)

    label_save_file = os.path.join(saveTxt,filename+'.txt')
    objects = []
    for shape in shapes:

        obj = {}
        obj['label'] = clsDict[shape[0]]
        obj['rbbox'] = shape[1]
        objects.append(obj)

    simpletxt_dump(objects, label_save_file, encode='rbbox')
    print(label_save_file)
