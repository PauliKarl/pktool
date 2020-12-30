from pktool import HRSCReaderCls, get_files, simpletxt_dump

dataset = ''

saveTxt = ''


clsReader = HRSCReaderCls(clsPath='E:\\code\\pktool\\tools\\dataset\\hrsc\\sysdata.xml', layer=2)

clsDict = clsReader.getclsDict()
print(clsDict)

xmlList=get_files(xmlFolder,_ends=['*.xml'])

for xmlfile in xmlList:
    basename = os.path.basename(xmlfile)
    filename, fmt = os.path.splitext(basename)

    shapes = clsReader.parseXML(xmlfile)

    label_save_file = os.path.join(saveTxt,'.txt')
    objects = {}
    objects['label'] = shapes[0]
    objects['rbbox'] = shapes[1]

    simpletxt_dump(objects, label_save_file, encode='rbbox')
    print(label_save_file)


