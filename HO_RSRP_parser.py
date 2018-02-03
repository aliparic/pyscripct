

from lxml import etree
from datetime import datetime
from  xml.etree.ElementTree import ElementTree
from pandas import DataFrame, HDFStore
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

#import pdb
#pdb.set_trace()

print ('hello')
def create_xml_conform_file(xml_file):

    try:
        for event, elem in etree.iterparse(xml_file):
            elem.clear()

    except etree.XMLSyntaxError:
        new_xml_file=xml_file
        while os.path.exists(new_xml_file):
            new_xml_file += "_tmp"
        with open(xml_file) as _in, open(new_xml_file, 'w+') as _out:
            _out.write("<xml_data>")
            for line in _in:
                _out.write(line)
            _out.write("</xml_data>")
        xml_file=new_xml_file
    return xml_file


def Get_TimeStamp(node, type):

    global HO_time_list

    pairs=node.findall('pair')
    for tag in pairs:
        if tag.attrib['key'] == "timestamp":
            datetime_object=datetime.strptime(tag.text, '%Y-%m-%d %H:%M:%S.%f')
            print(datetime_object, type)
            HO_time_list.append([])
            HO_time_list[len(HO_time_list)-1].append(datetime_object)




#    for elem in node.getchildren():
#        printRecur(elem,type)


def Get_RSRP(node, type):
    global RSRP_list
    pairs=node.findall('pair')
    #RSRP_list.append([])
    for tag in pairs:
        if tag.attrib['key']=='RSRP(dBm)':
           import  ast
           RSRP_list.append(ast.literal_eval(tag.text))
           break


HO_time_list = []
RSRP_list=[]
cellID=[]

def Parse_Main(xml_file):

        xml_file=create_xml_conform_file(xml_file)
        tree=etree.ElementTree()
        tree.parse(xml_file)

        dm_packets = tree.findall('dm_log_packet')
        lastnode='fake'
        global cellID
        for node in dm_packets:
              for tag in node.iter():

                    types=['lte-rrc.targetPhysCellId', 'lte-rrc.rrcConnectionReconfigurationComplete_element', 'LTE_PHY_Connected_Mode_Intra_Freq_Meas']
                    if tag.get('name') in types:


                         if tag.get('name')=='lte-rrc.rrcConnectionReconfigurationComplete_element':
                            if lastnode =='lte-rrc.targetPhysCellId':
                                lastnode = tag.get('name')
                                Get_TimeStamp(node, tag.get('name'))



                         if tag.get('name') == 'lte-rrc.targetPhysCellId':
                                lastnode = tag.get('name')
                                #print (lastnode)
                                Get_TimeStamp(node, tag.get('name'))
                                #cellID.append(tag.get('showname'))
                                #tmp=tag.get('showname')
                                print (int(tag.get('show')))
                                cellID.append(int(tag.get('show')))
                                #pos = tmp.find(":")
                                #cellID.append(tmp[pos+1:])




                    if tag.text=='LTE_PHY_Connected_Mode_Intra_Freq_Meas':
                         Get_RSRP(node, tag.get('text'))

        global path
        command= "rm "+ path + '/*_tmp'
        os.system(command)

        i=0
        j=0
        HO_time=[]
        HO_interval=[]
        while i <= len(HO_time_list)-3:

             HO_time.append(int((HO_time_list[i+1][0]- HO_time_list[i][0]).total_seconds() * 1000))
             HO_interval.append(int((HO_time_list[i + 2][0] - HO_time_list[i][0]).total_seconds() ))
             i=i+2
             j=j+1


        print (HO_time)
        print (HO_interval)
        #return HO_time
        return HO_time, HO_interval


if __name__=="__main__":

    paths = ['./rmbt/498/CubicMobile']
    paths = ['./m498/']
    #paths=['./http/386/']
    HO=0
    count=1
    for path in paths:
            xml_files = [pos_xml for pos_xml in os.listdir(path) if pos_xml.endswith('.xml')]
            for index, xml_file in enumerate(xml_files):
                print (xml_file)
                HO, HO_inter=Parse_Main(os.path.join(path,xml_file))   # counting the HO latancy and their interarrival time
            print (HO)
            print(cellID)


    plt.figure(1)
    plt.xlim([-150, -50])
    sorted_ = np.sort(RSRP_list)
    yvals = np.arange(len(sorted_)) / float(len(sorted_))
    plt.plot(sorted_, yvals)
    plt.xlabel('samples')
    plt.ylabel('RSRP value')

    plt.figure(2)
    plt.plot(RSRP_list)

    plt.show()




