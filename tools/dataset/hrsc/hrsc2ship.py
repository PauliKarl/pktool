from pktool import HRSCReaderCls, get_files, simpletxt_dump, mkdir_or_exist, thetaobb2pointobb
import os

clsPath='/home/pd/code/pktool/tools/dataset/hrsc/sysdata.xml'
datasets=['test','trainval']

instances = 0

for dataset in datasets:

    xmlFolder = '/data/hrsc2016/release/v0/{}/annotations/'.format(dataset)

    # saveTxt = '/data/pd/hrsc2016/ship/v0/{}/annotations/'.format(dataset)
    saveTxt = '/data2/pd/sdc/shipdet/hrsc2016/v0/{}/labels/'.format(dataset)
    mkdir_or_exist(saveTxt)

    clsReader = HRSCReaderCls(clsPath=clsPath, layer=2)

    clsDict = clsReader.getclsDict()
    print(clsDict)

    xmlList,num=get_files(xmlFolder,_ends=['*.xml'])
    print(num)
    for xmlfile in xmlList:
        basename = os.path.basename(xmlfile)
        filename, fmt = os.path.splitext(basename)

        shapes = clsReader.parseXML(xmlfile)

        label_save_file = os.path.join(saveTxt,filename+'.txt')
        objects = []
        for shape in shapes:
            instances+=1
            obj = {}
            obj['label'] = 'ship'#clsDict[shape[0]]
            obj['pointobb'] = thetaobb2pointobb(shape[1])
            objects.append(obj)


        simpletxt_dump(objects, label_save_file, encode='pointobb')
        # print(label_save_file)
    print(clsReader.MaxImgWidth,clsReader.MinImgWidth)
