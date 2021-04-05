from pktool import fair1m_parse,get_files,simpletxt_dump, mkdir_or_exist
import os
FilteredCLASSES = ['Passenger Ship', 'Motorboat', 'Fishing Boat', 'Tugboat', 'Engineering Ship', 'Liquid Cargo Ship', "Dry Cargo Ship", 'Warship', 'other-ship']

xml_path = '/data2/pd/fair1m/train/part1/labelXmls/'
filtered_label_path = '/data2/pd/sdc/shipdet/fair1m/v0/trainval/labels/'
mkdir_or_exist(filtered_label_path)


xmlList,num=get_files(xml_path,_ends=['*.xml'])
cls_fair1m ={}
print(num)
filter_count = 1
have_count = 0
for idx, xmlfile in enumerate(xmlList):
    print(idx, xmlfile)
    objects = fair1m_parse(xmlfile)
    filtered_objects = []
    
    for single_object in objects:
        # if label not in cls_fair1m:
        #     cls_fair1m[label]=1
        # else:
        #     cls_fair1m[label]+=1

        if single_object['label'] in FilteredCLASSES:
            have_count+=1
            single_object['label'] = 'ship'#single_object['label']
            filtered_objects.append(single_object)
        else:
            filter_count+=1
            continue
        if len(filtered_objects) > 0:
            simpletxt_dump(filtered_objects, os.path.join(filtered_label_path, os.path.split(xmlfile)[-1].split('.xml')[0] + '.txt'),encode='points')

print("\nFilter object counter: {}".format(filter_count))
print("ship object counter: {}".format(have_count))
