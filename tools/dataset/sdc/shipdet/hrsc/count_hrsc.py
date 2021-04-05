from pktool import HRSCReaderCls, simpletxt_parse,get_files
import os


clsPath='/home/pd/code/pktool/tools/dataset/hrsc/sysdata.xml'

clsReader = HRSCReaderCls(clsPath=clsPath, layer=2)

clsDict = clsReader.getclsDict()

count_dict = {}
# print(clsDict)

datasets = ['test', 'trainval']

for dataset in datasets:

    xmlFolder = '/data/hrsc2016/release/v0/{}/annotations/'.format(dataset)

    xmlList,num=get_files(xmlFolder,_ends=['*.xml'])
    print(num)

    for xmlfile in xmlList:
        basename = os.path.basename(xmlfile)
        filename, fmt = os.path.splitext(basename)

        shapes = clsReader.parseXML(xmlfile)

        # objects = simpletxt_parse(txtPath,boxType='thetaobb')
        for shape in shapes:
            if clsDict[shape[0]] not in count_dict:
                count_dict[clsDict[shape[0]]]=1
            else:
                count_dict[clsDict[shape[0]]]+=1

print(count_dict)
    


