from pktool import get_files,mask2rbbox
import xml.etree.ElementTree as ET
import json

def coco_analysze(jsonFile):
    '''
        "images": [
        {
            "date_captured": "2019",
            "file_name": "Airbus_c5931b345.png",
            "height": 768,
            "id": 1,
            "license": 1,
            "url": "http://jwwangchn.cn",
            "width": 768
        },
    '''
    with open(jsonFile,'r',encoding='utf-8') as f:
        annsDict = json.load(f)

    imgDict=annsDict['images']

    print('imageNum is {}'.format(len(imgDict)))

    infos={'small':0,'medium':0 , 'large':0}

    for i in range(len(annsDict['annotations'])):
        instanceObject = annsDict['annotations'][i]
        area = instanceObject['area']
        if area<1024:
            infos['small']+=1
        elif area>9216:
            infos['large']+=1
        else:
            infos['medium']+=1
    print('smallObjectNum is {}'.format(infos['small']))
    print('mediumObjectNum is {}'.format(infos['medium']))
    print('largeObjectNum is {}'.format(infos['large']))
    



    


def data_analysze_xml(origin_label_path):
    """images|instances|scales|ratios|object sizes
    Args:
        origin_label_path: annotation path .xml format
            <annotation>
                <folder>VOC2007</folder>
                <filename>Airbus_000194a2d.png</filename>
                <size>
                    <width>768</width>
                    <height>768</height>
                    <depth>3</depth>
                </size>
                <object>
                    <name>ship</name>
                    <pose>Unspecified</pose>
                    <truncated>0</truncated>
                    <difficult>0</difficult>
                    <bndbox>
                        <xmin>469</xmin>
                        <ymin>287</ymin>
                        <xmax>492</xmax>
                        <ymax>307</ymax>
                    </bndbox>
                </object>
            <annotation>
    Return:
        infos: (list)[dataset_info], 1xlen(datasets),
            dataset_info = {}
            dataset_info['type'] = dataset
            dataset_info['images'] = len(label_list)
            dataset_info['instances'] = {'total':0, 'small':0, 'large':0, 'ratios':[]}
            dataset_info['image_sizes'] = image_sizes
    """
    #datasets = ['Airbus','DIOR','DOTA','HRSC','LEVIR','MASATI','RS','xView','NWPU']
    
    
    datasets = ['Airbus']

    infos = []
    for dataset in datasets:
        
        label_list,num = get_files(origin_label_path,_ends=['{}*.xml'.format(dataset)])
        print(num)

        object_instances={'total':0, 'small':0, 'large':0, 'ratios':[]}
        # ratios = [1:5,1:3,1:1,3:1,5:1]
        ratios=[0,0,0,0,0,0]
        image_sizes = []
        for labelfile in label_list:
            tree = ET.parse(labelfile)
            root = tree.getroot()
            objects = []
            img_size = root.find('size')
            img_width = float(img_size.find('width').text)
            img_height = float(img_size.find('height').text)
            if (img_width,img_height) not in image_sizes:
                image_sizes.append((img_width,img_height))


            for single_object in root.findall('object'):

                object_instances['total']+=1

                bndbox = single_object.find('bndbox')

                xmin = float(bndbox.find('xmin').text)
                ymin = float(bndbox.find('ymin').text)
                xmax = float(bndbox.find('xmax').text)
                ymax = float(bndbox.find('ymax').text)
                obj_width = xmax-xmin+1
                obj_height = ymax-ymin+1

                
                if obj_height*obj_width<1024:
                    object_instances['small']+=1
                elif obj_height*obj_width>9216:
                    object_instances['large']+=1
                

                ratio = obj_width/obj_height
                if ratio<=0.2:
                    ratios[0]+=1
                elif ratio<=1/3:
                    ratios[1]+=1
                elif ratio<=1:
                    ratios[2]+=1
                elif ratio<=3:
                    ratios[3]+=1
                elif ratio<=5:
                    ratios[4]+=1
                else:
                    ratios[5]+=1

        object_instances['ratios']=ratios

        dataset_info = {}
        dataset_info['type'] = dataset
        dataset_info['images'] = len(label_list)
        dataset_info['instances'] = object_instances
        dataset_info['image_sizes'] = image_sizes

        infos.append(dataset_info)
    return infos




if __name__ == '__main__':

    '''
    jsonFile = '/data2/ghw/ship/coco/annotations/instances_val2017.json'
    coco_analysze(jsonFile)
    '''
    origin_image_path = '/data/zrx/ShipDatasetv1/VOC2012/JPEGImages/'
    origin_label_path = '/data/zrx/ShipDatasetv1/misc_file/xml/'

    infos = data_analysze_xml(origin_label_path)
    total_images = 0
    total_instances = 0
    small = 0
    big = 0
    ratios = [0,0,0,0,0,0]
    for info in infos:
        total_images+=info['images']
        total_instances+=info['instances']['total']
        small+=info['instances']['small']
        big+=info['instances']['large']
        ratio = info['instances']['ratios']
        for i in range(6):
            ratios[i]+=ratio[i]
        
        print('small in {}:'.format(info['type']),info['instances']['small'])
        print('large in {}:'.format(info['type']),info['instances']['large'])
        # print('imageSize in {}: is '.format(info['type']), info['image_sizes'])
    print("total_images:",total_images)
    print("total_instances:",total_instances)
    print("small:",small/total_instances)
    print("large:",big/total_instances)
    print("ratios:",ratios)