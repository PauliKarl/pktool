from pktool import  get_files, simpletxt_dump, simpletxt_parse,mkdir_or_exist
import os

instances = 0
labelFolder = '/data2/pd/sdc/shipdet/ext/v0/origintxt/'
saveTxt = '/data2/pd/sdc/multidet/ext/v0/trainval/labels'
mkdir_or_exist(saveTxt)
convert_classes = {'巡洋舰': 'Cruiser', '驱逐舰': 'Destroyer', '航母-里根号': 'Aircraft carrier', '两栖指挥舰-蓝岭号': 'Command ship', '直升机驱逐舰': 'Destroyer', '补给舰': 'Warship', 'ship': 'Ship', '潜艇': 'Submarine', '运输舰': 'Warship', '两栖攻击舰': 'Amphibious ship', '船坞登陆舰': 'Warship', '护卫舰': 'Frigate', '两栖运输舰-大隅级': 'Amphibious ship', '两栖运输舰': 'Amphibious ship', '船坞运输舰': 'Warship', '航母': 'Aircraft carrier', '濒海战斗舰': 'Warship', '两栖运输舰-大隅号': 'Amphibious ship'}

xmlList,num=get_files(labelFolder,_ends=['*.txt'])
print(num)
for xmlfile in xmlList:
    basename = os.path.basename(xmlfile)
    filename, fmt = os.path.splitext(basename)

    shapes = simpletxt_parse(xmlfile,boxType='points')

    label_save_file = os.path.join(saveTxt,filename+'.txt')
    objects = []
    for shape in shapes:
        instances+=1
        obj = {}
        obj['label'] = convert_classes[shape['label']]
        obj['points'] = shape['points']
        objects.append(obj)

    simpletxt_dump(objects, label_save_file, encode='points')
    print(label_save_file)