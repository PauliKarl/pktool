import os
from pktool import XVIEW_PARSE

if __name__ == '__main__':
    # get ship object in xView datasets    
    Maritime_label = {'Maritime Vessel', 'Motorboat', 'Sailboat', 'Tugboat', 'Barge', 'Fishing Vessel', 'Ferry', 'Yacht', 'Container Ship','Oil Tanker'}
    num_obj = {'Maritime Vessel':0, 'Motorboat':0, 'Sailboat':0, 'Tugboat':0, 'Barge':0, 'Fishing Vessel':0, 'Ferry':0, 'Yacht':0, 'Container Ship':0,'Oil Tanker':0}
    data_parser = XVIEW_PARSE("/data2/zrx/xView/xView_train.geojson","/home/pd/code/generate_dataset/xview/xview_class_labels.txt")
    img_list = set(data_parser.image_names)
    for img in img_list:
        if img == "None":
            continue
        obj = data_parser.xview_parse(img)
        if len(obj):
            f_name = img.split(".")[0]
            f_path = "/data/pd/xview/shiptxt/"+f_name+".txt"

            f = open(f_path,mode="w")
            no_ship_flag = True
            for instance in obj:
                if instance["label"] not in Maritime_label:
                    continue
                no_ship_flag = False
                bbox = instance["bbox"]
                #统计示例个数
                num_obj[instance["label"]]+=1

                f.write(str(bbox[0])+","+str(bbox[1])+","+
                        str(bbox[2])+","+str(bbox[3])+","+ instance["label"] + "\n")
            f.close()
            if no_ship_flag:
                os.remove(f_path)
    print(num_obj)
    '''
    data_parser = XVIEW_PARSE("/home/pt/data/xView/xView_train.geojson","/home/pt/project/wwtool/tools/datasets/xview/xview_class_labels.txt")
    img_list = set(data_parser.image_names)
    label_list = set()

    for img in img_list:
        if img == "None":
            continue
        obj = data_parser.xview_parse(img)
        if len(obj):
            for instance in obj:
                label_list.add(instance["label"])

    print(label_list)
'''