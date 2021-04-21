import itertools
import logging
import os.path as osp
import tempfile
from collections import OrderedDict
import json
import mmcv
import numpy as np
from mmcv.utils import print_log
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from terminaltables import AsciiTable
import os
from mmdet.core import eval_recalls

r"""
1.先通过test.json文件获取图像与对应ID
2.将检测结果存为coco格式的json文件：主要修改results2json(results, outfile_prefix)让检测结果能正确写入json
"""
# CLASSES = ('ship', )
# IMG_FORMAT = ''

##AerialDetection结果文件图像带后缀，IMG_FORMAT = ''
##Rotation中IMG_FORMAT = '.png'

def load_imgID_and_catID(test_json_file):
    img_and_ID = {}
    cat_and_ID = {}
    with open(test_json_file,'r',encoding='utf-8') as f:
        annsDict = json.load(f)
    imgDict = annsDict['images']
    catDict = annsDict['categories']
    for c in range(len(catDict)):
        className = catDict[c]['name']
        cat_and_ID[className] = catDict[c]['id']
    for i in range(len(imgDict)):
        imgName = imgDict[i]['file_name']
        img_and_ID[imgName] = imgDict[i]['id']
    return img_and_ID,cat_and_ID


def points2xywh(points):
    """Convert ``xyxy`` style bounding boxes to ``xywh`` style for COCO
    evaluation.

    Args:
        bbox (numpy.ndarray): The bounding boxes, shape (4, ), in
            ``xyxy`` order.

    Returns:
        list[float]: The converted bounding boxes, in ``xywh`` order.
    """
    xmin = min(points[0::2])
    ymin = min(points[1::2])
    xmax = max(points[0::2])
    ymax = max(points[1::2])
    bbox_w = xmax - xmin
    bbox_h = ymax - ymin

    return [xmin,ymin,bbox_w,bbox_h]

def read_res_txt(res_txt_file):
    results = {}
    with open(res_txt_file,'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split(' ') for x in lines]
        for splitline in splitlines:
            imgName = splitline[0]+IMG_FORMAT

            if imgName not in results:
                results[imgName] = [[],[]]##[list[scores],list[points]]
            else:
                results[imgName][0].append(float(splitline[1]))
                results[imgName][1].append([float(ponit) for ponit in splitline[2:]])
    return results
    # xmin = min(points[0::2])
    # ymin = min(points[1::2])
    # xmax = max(points[0::2])
    # ymax = max(points[1::2])
    # bbox_w = xmax - xmin
    # bbox_h = ymax - ymin

def _segm2json(results,img_and_ID,cat_and_ID):
    """Convert instance segmentation results to COCO json style."""
    bbox_json_results = []
    segm_json_results = []
    for catID,cat_result in enumerate(results):
        for imgName,result in cat_result.items():##获取单个图像的检测结果result
            img_id = img_and_ID[imgName]
            scores, dets = result[0],result[1]
            # det, seg = cat_result[idx]##获取单个图像的检测结果
            for idx in range(len(scores)):##单个图像中每个类别的检测结果遍历
                # bbox and segm results
                points = dets[idx]##获取单个类别的检测结果，即某一图像上某一类的预测结果

                data = dict()
                data['image_id'] = img_id
                data['bbox'] = points2xywh(points)##
                data['score'] = float(scores[idx])
                data['category_id'] = catID+1 ##
                data['segmentation'] = points
                bbox_json_results.append(data)

            for idx in range(len(scores)):##单个图像中每个类别的检测结果遍历
                #segm results
                points = dets[idx]##获取单个类别的检测结果，即某一图像上某一类的预测结果

                data = dict()
                data['image_id'] = img_id
                data['bbox'] = points2xywh(points)##
                data['score'] = float(scores[idx])
                data['category_id'] = catID+1 ##
                data['segmentation'] = [points]
                segm_json_results.append(data)

    return bbox_json_results, segm_json_results

def results2json(results, outfile_prefix):
    ##主要修改这个文件是的检测结果能正确写入json
    """Dump the detection results to a COCO style json file.

    There are 3 types of results: proposals, bbox predictions, mask
    predictions, and they have different data types. This method will
    automatically recognize the type, and dump them to json files.

    Args:
        results (list[list | tuple | ndarray]): Testing results of the
            dataset.
        outfile_prefix (str): The filename prefix of the json files. If the
            prefix is "somepath/xxx", the json files will be named
            "somepath/xxx.bbox.json", "somepath/xxx.segm.json",
            "somepath/xxx.proposal.json".

    Returns:
        dict[str: str]: Possible keys are "bbox", "segm", "proposal", and \
            values are corresponding filenames.
    """
    result_files = dict()

    json_results = _segm2json(results)
    result_files['bbox'] = f'{outfile_prefix}.bbox.json'
    result_files['segm'] = f'{outfile_prefix}.segm.json'
    mmcv.dump(json_results[0], result_files['bbox'])
    mmcv.dump(json_results[1], result_files['segm'])

    return result_files

def format_results_bak(results, jsonfile_prefix=None, **kwargs):
    """Format the results to json (standard format for COCO evaluation).

    Args:
        results (list[tuple | numpy.ndarray]): Testing results of the
            dataset.
        jsonfile_prefix (str | None): The prefix of json files. It includes
            the file path and the prefix of filename, e.g., "a/b/prefix".
            If not specified, a temp file will be created. Default: None.

    Returns:
        tuple: (result_files, tmp_dir), result_files is a dict containing \
            the json filepaths, tmp_dir is the temporal directory created \
            for saving json files when jsonfile_prefix is not specified.
    """
    result_files = results2json(results, jsonfile_prefix)
    return result_files

def format_results(results,jsonfile_prefix=None,img_and_ID=None,cat_and_ID=None):
    ##目前实现单类结果写入
    result_files = dict()
    json_results = _segm2json(results,img_and_ID,cat_and_ID)
    if jsonfile_prefix is None:
        tmp_dir = tempfile.TemporaryDirectory()
        jsonfile_prefix = osp.join(tmp_dir.name, 'results')
    else:
        tmp_dir = None

    result_files['bbox'] = f'{outfile_prefix}.bbox.json'
    result_files['proposal'] = f'{outfile_prefix}.bbox.json'
    result_files['segm'] = f'{outfile_prefix}.segm.json'
    mmcv.dump(json_results[0], result_files['bbox'])
    mmcv.dump(json_results[1], result_files['segm'])
    return result_files,tmp_dir


def evaluate(   ann_file,
                result_files,
                metric='bbox',
                logger=None,
                jsonfile_prefix=None,
                classwise=False,
                proposal_nums=(100, 300, 1000),
                iou_thrs=None,
                metric_items=None):
    """Evaluation in COCO protocol.

    Args:
        results (list[list | tuple]): Testing results of the dataset.
        metric (str | list[str]): Metrics to be evaluated. Options are
            'bbox', 'segm', 'proposal', 'proposal_fast'.
        logger (logging.Logger | str | None): Logger used for printing
            related information during evaluation. Default: None.
        jsonfile_prefix (str | None): The prefix of json files. It includes
            the file path and the prefix of filename, e.g., "a/b/prefix".
            If not specified, a temp file will be created. Default: None.
        classwise (bool): Whether to evaluating the AP for each class.
        proposal_nums (Sequence[int]): Proposal number used for evaluating
            recalls, such as recall@100, recall@1000.
            Default: (100, 300, 1000).
        iou_thrs (Sequence[float], optional): IoU threshold used for
            evaluating recalls/mAPs. If set to a list, the average of all
            IoUs will also be computed. If not specified, [0.50, 0.55,
            0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95] will be used.
            Default: None.
        metric_items (list[str] | str, optional): Metric items that will
            be returned. If not specified, ``['AR@100', 'AR@300',
            'AR@1000', 'AR_s@1000', 'AR_m@1000', 'AR_l@1000' ]`` will be
            used when ``metric=='proposal'``, ``['mAP', 'mAP_50', 'mAP_75',
            'mAP_s', 'mAP_m', 'mAP_l']`` will be used when
            ``metric=='bbox' or metric=='segm'``.

    Returns:
        dict[str, float]: COCO style evaluation metric.
    """

    metrics = metric if isinstance(metric, list) else [metric]
    allowed_metrics = ['bbox', 'segm']
    for metric in metrics:
        if metric not in allowed_metrics:
            raise KeyError(f'metric {metric} is not supported')
    if iou_thrs is None:
        iou_thrs = np.linspace(
            .5, 0.95, int(np.round((0.95 - .5) / .05)) + 1, endpoint=True)
    if metric_items is not None:
        if not isinstance(metric_items, list):
            metric_items = [metric_items]

    # result_files = format_results(results, jsonfile_prefix)

    eval_results = OrderedDict()
    coco = COCO(ann_file)
    cocoGt = coco
    for metric in metrics:
        msg = f'Evaluating {metric}...'
        if logger is None:
            msg = '\n' + msg
        print_log(msg, logger=logger)


        if metric not in result_files:
            raise KeyError(f'{metric} is not in results')
        try:
            cocoDt = cocoGt.loadRes(result_files[metric])
        except IndexError:
            print_log(
                'The testing results of the whole dataset is empty.',
                logger=logger,
                level=logging.ERROR)
            break

        iou_type = 'bbox' if metric == 'proposal' else metric
        cocoEval = COCOeval(cocoGt, cocoDt, iou_type)
        cocoEval.params.catIds = coco.get_cat_ids(cat_names=CLASSES)
        cocoEval.params.imgIds = coco.get_img_ids()
        cocoEval.params.maxDets = list(proposal_nums)
        cocoEval.params.iouThrs = iou_thrs
        # mapping of cocoEval.stats
        coco_metric_names = {
            'mAP': 0,
            'mAP_50': 1,
            'mAP_75': 2,
            'mAP_s': 3,
            'mAP_m': 4,
            'mAP_l': 5,
            'AR@100': 6,
            'AR@300': 7,
            'AR@1000': 8,
            'AR_s@1000': 9,
            'AR_m@1000': 10,
            'AR_l@1000': 11
        }
        if metric_items is not None:
            for metric_item in metric_items:
                if metric_item not in coco_metric_names:
                    raise KeyError(
                        f'metric item {metric_item} is not supported')

        if metric == 'proposal':
            cocoEval.params.useCats = 0
            cocoEval.evaluate()
            cocoEval.accumulate()
            cocoEval.summarize()
            if metric_items is None:
                metric_items = [
                    'AR@100', 'AR@300', 'AR@1000', 'AR_s@1000',
                    'AR_m@1000', 'AR_l@1000'
                ]

            for item in metric_items:
                val = float(
                    f'{cocoEval.stats[coco_metric_names[item]]:.3f}')
                eval_results[item] = val
        else:
            cocoEval.evaluate()
            cocoEval.accumulate()
            cocoEval.summarize()
            if classwise:  # Compute per-category AP
                # Compute per-category AP
                # from https://github.com/facebookresearch/detectron2/
                precisions = cocoEval.eval['precision']
                # precision: (iou, recall, cls, area range, max dets)
                assert len(coco.get_cat_ids(cat_names=CLASSES)) == precisions.shape[2]

                results_per_category = []
                for idx, catId in enumerate(coco.get_cat_ids(cat_names=CLASSES)):
                    # area range index 0: all area ranges
                    # max dets index -1: typically 100 per image
                    nm = coco.loadCats(catId)[0]
                    precision = precisions[:, :, idx, 0, -1]
                    precision = precision[precision > -1]
                    if precision.size:
                        ap = np.mean(precision)
                    else:
                        ap = float('nan')
                    results_per_category.append(
                        (f'{nm["name"]}', f'{float(ap):0.3f}'))

                num_columns = min(6, len(results_per_category) * 2)
                results_flatten = list(
                    itertools.chain(*results_per_category))
                headers = ['category', 'AP'] * (num_columns // 2)
                results_2d = itertools.zip_longest(*[
                    results_flatten[i::num_columns]
                    for i in range(num_columns)
                ])
                table_data = [headers]
                table_data += [result for result in results_2d]
                table = AsciiTable(table_data)
                print_log('\n' + table.table, logger=logger)

            if metric_items is None:
                metric_items = [
                    'mAP', 'mAP_50', 'mAP_75', 'mAP_s', 'mAP_m', 'mAP_l'
                ]

            for metric_item in metric_items:
                key = f'{metric}_{metric_item}'
                val = float(
                    f'{cocoEval.stats[coco_metric_names[metric_item]]:.3f}'
                )
                eval_results[key] = val
            ap = cocoEval.stats[:6]
            eval_results[f'{metric}_mAP_copypaste'] = (
                f'{ap[0]:.3f} {ap[1]:.3f} {ap[2]:.3f} {ap[3]:.3f} '
                f'{ap[4]:.3f} {ap[5]:.3f}')
    return eval_results



if __name__=='__main__':
    # CLASSES = ('ship', )
    CLASSES=('Cargo vessel','Ship','Motorboat','Fishing boat','Destroyer','Tugboat','Loose pulley','Warship','Engineering ship','Amphibious ship','Cruiser','Frigate','Submarine','Aircraft carrier','Hovercraft','Command ship')
    IMG_FORMAT = ''
    
    test_json_file = "/data2/pd/sdc/multidet/v0/coco/annotations/sdc_test_v0.json"
    # results_dir='/data2/pd/sdc/multidet/v0/works_dir/aedet/faster_rcnn_RoITrans_r50_fpn_1x_shipdet/Task1_results_nms/'
    results_dir = '/data2/pd/sdc/multidet/v0/works_dir/aedet/faster_rcnn_obb_r50_fpn_1x_multidet/Task1_results_nms/'
    # results_txt='/data2/pd/sdc/multidet/v0/works_dir/aedet/faster_rcnn_obb_r50_fpn_1x_multidet/Task1_results_nms/Ship.txt'

    # results_txt = '/data2/pd/sdc/shipdet/v1/works_dir/rcenter/res50/ship.txt'#'0.040 0.164 0.008 0.017 0.065 0.042')
    # results_txt = '/home/pd/RotationDetection/tools/r3det/test_dota/FPN_Res50_r3det_1x_20210405/dota_res/Task1_ship.txt'
    # results_txt = "/data2/pd/sdc/shipdet/v1/works_dir/aedet/retinanet_obb_r50_fpn_1x_shipdet/Task1_results_nms/person.txt"
    # results_txt = "/data2/pd/sdc/shipdet/v0/rotationDet/test_dota/FPN_Res50_sdc_1x_20210403/dota_res_r/Task1_ship.txt"
    outfile_prefix = None#'/data2/pd/sdc/multidet/v0/works_dir/aedet/faster_rcnn_obb_r50_fpn_1x_multidet/result'
    # outfile_prefix = results_txt.split('.txt')[0]

    img_and_ID,cat_and_ID=load_imgID_and_catID(test_json_file)
    print(cat_and_ID)
    results_all_cat = []
    for cat in CLASSES:
        result_txt = results_dir + cat + '.txt'
        result = read_res_txt(result_txt)
        results_all_cat.append(result)
    
    result_files,tmp_dir = format_results(results_all_cat,jsonfile_prefix=outfile_prefix,img_and_ID=img_and_ID,cat_and_ID=cat_and_ID)

    eval_results = evaluate(test_json_file,
                            result_files,
                            metric='segm',#'segm','bbox'
                            jsonfile_prefix=None,
                            classwise=True,
                            proposal_nums=(100, 300, 1000))
    if tmp_dir is not None:
        tmp_dir.cleanup()
    print(eval_results)