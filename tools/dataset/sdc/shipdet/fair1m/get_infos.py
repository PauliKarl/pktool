from pktool import fair1m_parse, get_files

cls_fair1m = {}

xml_path = '/data2/pd/fair1m/train/part1/labelXmls/'

xmlList,num=get_files(xml_path,_ends=['*.xml'])

print(num)

for xmlfile in xmlList:
    objects = fair1m_parse(xmlfile)

    for single_object in objects:
        label = single_object['label']
        if label not in cls_fair1m:
            cls_fair1m[label]=1
        else:
            cls_fair1m[label]+=1

print(cls_fair1m)

# {'Boeing737': 375, 'A321': 269, 'A220': 478, 'other-airplane': 574, 'Small Car': 32887, 'Van': 29973, 'Dump Truck': 4618, 'other-vehicle': 1259, 'Motorboat': 1458, 'Cargo Truck': 2671, 'Intersection': 1285, 'Liquid Cargo Ship': 430, 'other-ship': 654, 'Baseball Field': 149, 'Tennis Court': 410, 'Football Field': 132, 'C919': 3, 'Bus': 309, 'Truck Tractor': 213, 'Excavator': 240, 'Fishing Boat': 762, 'Tugboat': 347, 'Dry Cargo Ship': 2155, 'Passenger Ship': 289, 'Basketball Court': 67, 'Engineering Ship': 288, 'ARJ21': 18, 'Trailer': 216, 'Bridge': 53, 'Boeing777': 24, 'Warship': 93, 'Tractor': 67, 'Boeing747': 37, 'A330': 58, 'A350': 15, 'Boeing787': 58, 'Roundabout': 4}

# ship = {'Passenger Ship': 289, 'Motorboat':1458, 'Fishing Boat':762, 'Tugboat':347, 'Engineering Ship':288, 'Liquid Cargo Ship':430, 'dry cargo ship':2155, 'warship':93, 'other-ship':654}
#9 CLASSES, 6476 instances

