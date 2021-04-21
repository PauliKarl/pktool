from pycocotools.coco import COCO   

import json
CLASSES = ('Cargo vessel','Ship','Motorboat','Fishing boat','Destroyer','Tugboat','Loose pulley','Warship','Engineering ship','Amphibious ship','Cruiser','Frigate','Submarine','Aircraft carrier','Hovercraft','Command ship')
def load_annotations(ann_file):
    """Load annotation from COCO style annotation file.

    Args:
        ann_file (str): Path of annotation file.

    Returns:
        list[dict]: Annotation info from COCO api.
    """

    coco = COCO(ann_file)
    cat_ids = coco.get_cat_ids(cat_names=CLASSES)
    cat2label = {cat_id: i for i, cat_id in enumerate(cat_ids)}
    img_ids = coco.get_img_ids()
    data_infos = []
    for i in img_ids:
        info = coco.load_imgs([i])[0]
        info['filename'] = info['file_name']
        data_infos.append(info)
    return data_infos


if __name__=='__main__':
    ann_file = "/data2/pd/sdc/multidet/v0/works_dir/mmdet/detectorsmask_albu_mixup_mstrain_3x/results.segm.json"
    # data_infos=load_annotations(ann_file)
    # print('ok')

    with open(ann_file,'r',encoding='utf-8') as f:
        annsDict = json.load(f)

    print('ok')