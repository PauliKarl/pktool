import os
import six
import glob

def get_files(path, _ends=['*.json']):
    """find all file endwith _ends[list]
    Args:
        path: root dir
        _ends: list, all formats you need
    Return:
        all_files: file list, full path
        file_num: count
    """
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

def get_key(d, v):
    return [key for key, val in d.items() if val==v][0]