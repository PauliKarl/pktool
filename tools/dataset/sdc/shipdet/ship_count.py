from pktool import simpletxt_parse, get_files, pointobb2thetaobb
import os 

def count_all_dataset():
    datasets_type = ['dota2.0','hrsc2016','rs','ext','fair1m']
    datasets = ['test','trainval']

    total = [0,0,0,0]

    for dataset_type in datasets_type:
        for dataset in datasets:
            splited_label_path = '/data2/pd/sdc/shipdet/{}/v0/{}/labels/'.format(dataset_type,dataset)            
            if not os.path.exists(splited_label_path):
                print("skipping {}/{}".format(dataset_type,dataset))
                continue
            print("waiting...{}/{}".format(dataset_type,dataset))

            label_list,num = get_files(splited_label_path,_ends=["*.txt"])

            instances = 0
            smallShip = 0
            largeShip = 0

            for idx, labelFile in enumerate(label_list):
                #print(idx,labelFile)
                ships = simpletxt_parse(labelFile,boxType='points')
                for ship in ships:
                    instances+=1
                    points = ship['points']
                    thetabox = pointobb2thetaobb(points)
                    if thetabox[2]*thetabox[3]<1024:
                        smallShip+=1
                    elif thetabox[2]*thetabox[3]>9216:
                        largeShip+=1
        
            total[0]+=num
            total[1]+=instances
            total[2]+=smallShip
            total[3]+=largeShip
            print("{}:images {}, instances {}, smallShip {}, largeShip {}".format(dataset_type+'/'+dataset,num,instances,smallShip,largeShip))
    
    print("total:images {}, instances {}, smallShip {}, largeShip {}".format(total[0],total[1],total[2],total[3]))

def count_sdc_dataset():
    datasets_type = ['sdc']
    datasets = ['test','trainval']

    total = [0,0,0,0]

    for dataset_type in datasets_type:
        for dataset in datasets:
            splited_label_path = '/data2/pd/{}/shipdet/v0/{}/labels/'.format(dataset_type,dataset)            
            if not os.path.exists(splited_label_path):
                print("skipping {}/{}".format(dataset_type,dataset))
                continue
            print("waiting...{}/{}".format(dataset_type,dataset))

            label_list,num = get_files(splited_label_path,_ends=["*.txt"])

            instances = 0
            smallShip = 0
            largeShip = 0

            for idx, labelFile in enumerate(label_list):
                #print(idx,labelFile)
                ships = simpletxt_parse(labelFile,boxType='points')
                for ship in ships:
                    instances+=1
                    points = ship['points']
                    thetabox = pointobb2thetaobb(points)
                    if thetabox[2]*thetabox[3]<1024:
                        smallShip+=1
                    elif thetabox[2]*thetabox[3]>9216:
                        largeShip+=1
        
            total[0]+=num
            total[1]+=instances
            total[2]+=smallShip
            total[3]+=largeShip
            print("{}:images {}, instances {}, smallShip {}, largeShip {}".format(dataset_type+'/'+dataset,num,instances,smallShip,largeShip))
    
    print("total:images {}, instances {}, smallShip {}, largeShip {}".format(total[0],total[1],total[2],total[3]))

if __name__=='__main__':
    count_all_dataset()
    # count_sdc_dataset()
