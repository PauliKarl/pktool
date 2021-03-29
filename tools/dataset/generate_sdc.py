from pktool import mkdir_or_exist, shuffle_dataset
import os


if __name__=="__main__":
    datasets_type=['dota2.0','hrsc2016','rs','ext']
    datasets = ['test','trainval']
    #每子数据集都按照8：2的比例划分训练集和测试集        
    trainval_dir = '/data2/pd/sdc/shipdet/v0/trainval'
    test_dir = '/data2/pd/sdc/shipdet/v0/test'
    for dataset_type in datasets_type:
        for dataset in datasets:
            splited_dataset_path = '/data2/pd/sdc/shipdet/{}/v1/{}/'.format(dataset_type,dataset)
            if not os.path.exists(splited_dataset_path):
                print("skipping {}/{}".format(dataset_type,dataset))
                continue
            print("shuffle {}/{}".format(dataset_type,dataset))
            shuffle_dataset(splited_dataset_path,trainval_dir,test_dir)
    print('shuffle ok!')

    