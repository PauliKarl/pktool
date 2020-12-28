

def simpletxt_dump(objects, anno_file, space=' ', encode='bbox'):
    """dump object information to simple txt label files  and use 'utf-8' 
    
    Arguments:
        objects {dict} -- object information
        label_file {str} -- label file path
    
    Returns:
        None
    """
    with open(anno_file, 'w', encoding='utf-8') as f:
        for obj in objects:
            bbox = obj[encode]
            label = obj['label']
            bbox = [round(_, 3) for _ in map(float, bbox)]
            bbox = ["{:.4f}".format(_) for _ in bbox]
            content = " ".join(map(str, bbox))
            content = content + space + label + '\n'
            f.write(content)
    return 