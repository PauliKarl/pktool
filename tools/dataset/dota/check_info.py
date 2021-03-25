from pktool import get_files

datasetPath = '/data2/pd/sdc/shipdet/ext/v1/trainval/labels'
#'/data/dota/origin/train/labelTxt-v1.0/'

txtlist,num = get_files(datasetPath,_ends=['*.txt'])
print(num)