from pktool import HRSCReaderCls, simpletxt_parse,pointobb2thetaobb
import os

def count_sdc_multi():
    count_dict = {}
    image_number = 0

    instances = 0
    smallShip = 0
    largeShip = 0
    datasets_type = ['multidet']
    datasets = ['test','trainval']
    for dataset_type in datasets_type:
        for dataset in datasets:
            label_path = '/data2/pd/sdc/{}/v0/{}/labels/'.format(dataset_type,dataset)
            if not os.path.exists(label_path):
                print("skipping {}/{}".format(dataset_type,dataset))
                continue
            print("waiting...{}/{}".format(dataset_type,dataset))
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

def count_all_subdataset():
    count_dict = {}
    image_number = 0

    instances = 0
    smallShip = 0
    largeShip = 0
    datasets_type = ['hrsc2016','ext','fair1m']
    datasets = ['test','trainval']
    for dataset_type in datasets_type:
        for dataset in datasets:
            label_path = '/data2/pd/sdc/multidet/{}/v1/{}/labels/'.format(dataset_type,dataset)
            if not os.path.exists(label_path):
                print("skipping {}/{}".format(dataset_type,dataset))
                continue
            print("waiting...{}/{}".format(dataset_type,dataset))
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


if __name__=="__main__":
    # count_sdc_multi()
    count_all_subdataset()