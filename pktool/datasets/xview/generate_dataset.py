from pktool import mkdir_or_exist, shuffle_dataset

if __name__=="__main__":
    origin_dataset_dir = 'F:/data/ship_detection/xView/origin'
    trainval_dir = 'F:/data/ship_detection/xView/v1/trainval'
    test_dir = 'F:/data/ship_detection/xView/v1/test'
    shuffle_dataset(origin_dataset_dir,trainval_dir,test_dir)

    