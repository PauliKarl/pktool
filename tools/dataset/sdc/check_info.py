from pktool import get_files

sdc_type = 'shipdet'
dataset_type = '/'
dataset='trainval'



imgPath = '/data2/pd/sdc/{}/{}/v1/{}/images/'.format(sdc_type,dataset_type,dataset)
labelPath = '/data2/pd/sdc/{}/{}/v1/{}/labels/'.format(sdc_type,dataset_type,dataset)

_,img_num = get_files(imgPath,_ends=['*.png'])
_,labes_num = get_files(labelPath,_ends=['*.txt'])

assert img_num==labes_num, "imgs {} and labels {} are not corr".format(img_num,labes_num)
print("images:{}".format(img_num))