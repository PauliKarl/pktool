from pktool import mkdir_or_exist, shuffle_dataset
import os


if __name__=="__main__":
    datasets=['dota-v1.5','hrsc2016','rs','ext']
    #每子数据集都按照8：2的比例划分训练集和测试集

    for dataset in datasets:

        origin_dataset_dir = '/data/pd/{}/ship/v1/'.format(dataset)

        trainval_dir = '/data/pd/shipdet/v1/trainval'
        test_dir = '/data/pd/shipdet/v1/test'
        print('shuffle {}'.format(dataset))
        shuffle_dataset(origin_dataset_dir,trainval_dir,test_dir)

    