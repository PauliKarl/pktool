import os
import chardet
import codecs

dir_ = "/home/ubuntu/paulikarl/Java"

for i in range(7):
    sub_dir = dir_ + '/' + 'day2' + str(i)
    l = os.listdir(sub_dir)
    for f in l:
        words = os.path.join(sub_dir,f)
        name,fmt = os.path.splitext(f)
        if fmt == '.txt':
            newFile = os.path.join(sub_dir,name) + "utf8" + fmt 
            rf = codecs.open(words,'r','GBK')
            try:
                wf = rf.read()
                file_object = codecs.open(newFile,'w','utf-8')
                file_object.write(wf)
                print(i)
            except:
                pass
