from pktool import HRSCReaderCls, simpletxt_parse
import os


clsPath='/home/pd/code/pktool/tools/dataset/hrsc/sysdata.xml'

clsReader = HRSCReaderCls(clsPath=clsPath, layer=2)

clsDict = clsReader.getclsDict()

count_dict = {}
print(clsDict)

datasets = ['test', 'trainval']

for dataset in datasets:

    saveTxt = '/data/pd/hrsc2016/ship/v0/{}/annotations/'.format(dataset)

    for txtfile in os.listdir(saveTxt):
        txtPath = os.path.join(saveTxt,txtfile)

        objects = simpletxt_parse(txtPath,boxType='thetaobb')
        for obj in objects:
            if obj['label'] not in count_dict:
                count_dict[obj['label']]=1
            else:
                count_dict[obj['label']]+=1

print(count_dict)
    


