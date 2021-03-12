from pktool import HRSCReaderCls, simpletxt_parse,pointobb2thetaobb
import os


count_dict = {}
image_number = 0

instances = 0
smallShip = 0
largeShip = 0

label_path = '/data/pd/hrsc2016/multiship/v1/labels/'

for txtfile in os.listdir(label_path):
    txtPath = os.path.join(label_path,txtfile)
    image_number+=1
    objects = simpletxt_parse(txtPath,boxType='points')
    for obj in objects:

        instances+=1
        points = obj['points']
        thetabox = pointobb2thetaobb(points)
        if thetabox[2]*thetabox[3]<1024:
            smallShip+=1
        elif thetabox[2]*thetabox[3]>9216:
            largeShip+=1

        if obj['label'] not in count_dict:
            count_dict[obj['label']]=1
        else:
            count_dict[obj['label']]+=1

print(count_dict)
print(image_number)
print("instances {}, smallShip {}, largeShip {}".format(instances,smallShip,largeShip))