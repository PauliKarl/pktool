from pktool import HRSCReaderCls, simpletxt_parse
import os


count_dict = {}
image_number = 0

label_path = '/data/pd/hrsc2016/multiship/v1/labels/'

for txtfile in os.listdir(label_path):
    txtPath = os.path.join(label_path,txtfile)
    image_number+=1
    objects = simpletxt_parse(txtPath,boxType='points')
    for obj in objects:
        if obj['label'] not in count_dict:
            count_dict[obj['label']]=1
        else:
            count_dict[obj['label']]+=1

print(count_dict)
print(image_number)