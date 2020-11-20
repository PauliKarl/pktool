import os
import chardet
import codecs
from pktool import mkdir_or_exist
dir_ = "/home/pd/data/oldlabels"
save_path = "/home/pd/data/labels"
mkdir_or_exist(save_path)
for file_lab in os.listdir(dir_):

    words = os.path.join(dir_,file_lab)
    name,fmt = os.path.splitext(file_lab)
    if fmt == '.txt':
        newFile = os.path.join(save_path,name) + fmt 
        rf = codecs.open(words,'r','GBK')
        try:
            wf = rf.read()
            file_object = codecs.open(newFile,'w','utf-8')
            file_object.write(wf)
            print(i)
        except:
            pass
