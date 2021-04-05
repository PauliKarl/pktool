from pktool import HRSCReaderCls, get_files, simpletxt_dump, mkdir_or_exist, thetaobb2pointobb
import os

clsPath='/home/pd/code/pktool/tools/dataset/sdc/shipdet/hrsc/sysdata.xml'
datasets=['test','trainval']

instances = 0

for dataset in datasets:

    xmlFolder = '/data/hrsc2016/release/v0/{}/annotations/'.format(dataset)

    saveTxt = '/data2/pd/sdc/multidet/hrsc2016/v0/{}/labels/'.format(dataset)
    mkdir_or_exist(saveTxt)

    clsReader = HRSCReaderCls(clsPath=clsPath, layer=2)

    clsDict = clsReader.getclsDict()
    # print(clsDict)
    # {100000001: '船', 100000002: '航母', 100000003: '军舰', 100000004: '商船', 100000005: '尼米兹级航母', 100000006: '企业级航母', 100000007: '阿利伯克级驱逐舰', 100000008: '惠德贝岛级船坞登陆舰', 100000009: '佩里级护卫舰', 100000010: '圣安东尼奥级两栖船坞运输舰', 100000011: '提康德罗加级巡洋舰', 100000012: '小鹰级航母', 100000013: '俄罗斯库兹涅佐夫号航母', 100000014: '阿武隈级护卫舰', 100000015: '奥斯汀级两栖船坞运输舰', 100000016: '塔拉瓦级通用两栖攻击舰', 100000017: '蓝岭级指挥舰', 100000018: '集装箱货船', 100000019: '尾部OX头部圆指挥舰', 100000020: '运输汽车船([]==[])', 100000022: '气垫船', 100000024: '游艇', 100000025: '货船(_|.--.--|_]=', 100000026: '游轮', 100000027: '潜艇', 100000028: '琵琶形军舰', 100000029: '医疗船', 100000030: '运输汽车船(======|', 100000031: '福特级航空母舰', 100000032: '中途号航母', 100000033: '无敌级航空母舰'}
    convert_classes = {100000001: 'Ship', 100000002: 'Aircraft carrier', 100000003: 'Warship', 100000004: 'Ship', 100000005: 'Aircraft carrier', 100000006: 'Aircraft carrier', 100000007: 'Destroyer', 100000008: 'Warship', 100000009: 'Frigate', 100000010: 'Amphibious ship', 100000011: 'Cruiser', 100000012: 'Aircraft carrier', 100000013: 'Aircraft carrier', 100000014: 'Frigate', 100000015: 'Amphibious ship', 100000016: 'Amphibious ship', 100000017: 'Command ship', 100000018: 'Cargo vessel', 100000019: 'Command ship', 100000020: 'Cargo vessel', 100000022: 'Hovercraft', 100000024: 'Motorboat', 100000025: 'Cargo vessel', 100000026: 'Loose pulley', 100000027: 'Submarine', 100000028: 'Warship', 100000029: 'Ship', 100000030: 'Cargo vessel', 100000031: 'Aircraft carrier', 100000032: 'Aircraft carrier', 100000033: 'Aircraft carrier'}

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
            obj['label'] = convert_classes[shape[0]]
            obj['points'] = thetaobb2pointobb(shape[1])
            objects.append(obj)


        simpletxt_dump(objects, label_save_file, encode='points')
    print(instances)