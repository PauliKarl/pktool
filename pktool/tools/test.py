from pktool import mkdir_or_exist, shuffle_dataset

if __name__=="__main__":
    origin_dataset_dir = '/data/pd/xview/origin'
    trainval_dir = '/data/pd/xview/v2/trainval'
    test_dir = '/data/pd/xview/v2/test'
    shuffle_dataset(origin_dataset_dir,trainval_dir,test_dir)