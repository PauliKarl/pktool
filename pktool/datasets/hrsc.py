from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree


XML_EXT = '.xml'
class HRSCReaderCls:
    """processing anns with hrsc2016 dataset
        L1: ship
        L2: aircraft carrier,warcraft,merchant ship
        L3: 29 classes
    get the dict key for class_id, val for class_Name, acc Li
    only extract layer, others assign parent
    sysdata.xml format:
        HRS_Class_ID: parent_id
        Class_ID: class_id
        Class_Layer: layer [0,1,2 reps L1, L2, L3]
    """
    def __init__(self, clsPath, layer=0):
        self.clsPath = clsPath
        self.clsDict = {}
        self.layer = layer
        assert self.layer in [0,1,2],  "Unsupport layer, only for 0,1,2"


        self.__getClsDict()

    def getclsDict(self):
        return self.clsDict

    def __getClsDict(self):
        assert self.clsPath.endswith(XML_EXT), "Unsupport file format"
        parser = etree.XMLParser(encoding='utf-8')
        xmltree = ElementTree.parse(self.clsPath, parser=parser).getroot()
        for child in xmltree:
            tag = child.tag

            if tag == "HRSC_Classes":
                for HRSC_Class in child:
                    class_id = parent_id = 0
                    for class_elem in HRSC_Class:
                        if class_elem.tag == "Class_Layer":
                            layer = int(class_elem.text)
                        elif class_elem.tag == "Class_ID":
                            class_id = int(class_elem.text)
                        elif class_elem.tag == "HRS_Class_ID":
                            parent_id = class_elem.text
                        elif class_elem.tag == "Class_Name":
                            class_name = class_elem.text
                        
                    # Only handle class layer 1
                    # assign layer 2 class id to layer 1
                    if class_id not in self.clsDict:
                        if self.layer == 0:
                            self.clsDict[class_id] = 'ship'
                        elif self.layer == 1:
                            if layer in [0,1]:
                                self.clsDict[class_id] = class_name
                            elif layer == 2:
                                self.clsDict[class_id] = self.clsDict[int(parent_id)]
                        elif self.layer == 2:
                            self.clsDict[class_id] = class_name

    def parseXML(self, xmlFile):
        assert xmlFile.endswith(XML_EXT), "Unsupport file format"

        shapes = []
        #[class_id, robndbox]

        parser = etree.XMLParser(encoding='utf-8')
        xmltree = ElementTree.parse(xmlFile, parser=parser).getroot()
        HRSC_Objects = xmltree.find('HRSC_Objects')
        for HRSC_Object in HRSC_Objects.findall('HRSC_Object'):
            class_id = int(HRSC_Object.find('Class_ID').text)

            mbox_cx = float(robndbox.find('mbox_cx').text)
            mbox_cy = float(robndbox.find('mbox_cy').text)
            mbox_w = float(robndbox.find('mbox_w').text)
            mbox_h = float(robndbox.find('mbox_h').text)
            mbox_ang = float(robndbox.find('mbox_ang').text)

            robndbox = [mbox_cx, mbox_cy, mbox_w, mbox_h, mbox_ang]

            shapes.append([class_id, robndbox])
        
        return shapes



                
