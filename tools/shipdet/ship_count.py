from pktool import simpletxt_parse, get_files, pointobb2thetaobb

datasets = ['dota-v1.5','hrsc2016','rs','ext']

if __name__=='__main__':
    total = [0,0,0,0]
    for dataset in datasets:

        label_path = '/data/pd/{}/ship/v1/labels'.format(dataset)
        label_list,num = get_files(label_path,_ends=["*.txt"])

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
        print("{}:images {}, instances {}, smallShip {}, largeShip {}".format(dataset,num,instances,smallShip,largeShip))
    print("total:images {}, instances {}, smallShip {}, largeShip {}".format(total[0],total[1],total[2],total[3]))