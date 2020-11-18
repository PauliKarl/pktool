import os
import six
import glob

def get_files(path, _ends=['*.json']):
    all_files = []
    for _end in _ends:
        files = glob.glob(os.path.join(path, _end))
        all_files.extend(files)
    file_num = len(all_files)
    return all_files, file_num

def mkdir_or_exist(dir_name, mode=0o777):
    if dir_name == '':
        return
    dir_name = os.path.expanduser(dir_name)
    if six.PY3:
        os.makedirs(dir_name, mode=mode, exist_ok=True)
    else:
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name, mode=mode)