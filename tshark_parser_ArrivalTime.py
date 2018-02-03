
import os
import subprocess
from multiprocessing import Process, Manager
import matplotlib.pyplot as plt
import numpy as np
import csv
import time
import datetime
import dateutil.parser

if __name__=="__main__":


    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/ServerlogsCubic']
    for path in paths:
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           print(pcap_file)
           p=os.path.join(path, pcap_file)
           command = "tshark -r " + p + " -2  -R  '(ip.src == 46.194.104.156 and tcp) && !(tcp.analysis.out_of_order) && !(tcp.analysis.retransmission)' -T fields -e frame.time_epoch > outAT.csv"
           #command = "tshark -r " + p + " -2  -R  '(ip.src == 130.243.27.222) && (tcp.analysis.ack_rtt>0)' -T fields -e tcp.analysis.ack_rtt > out.csv"
           os.system(command)
           f = open('outAT.csv', "r")
           reader = csv.reader(f)
           ArrivalTime=[]
           first_row = next(reader)
           temp=float(first_row[0])
           for row in reader:
               #print (datetime_object)
               #ArrivalTime.append(row[0])
               #temp=datetime.datetime.now()
               #t=datetime.datetime.fromtimestamp(float(row[0])).strftime('%c')
               #print (float(row[0])-temp)
               #ArrivalTime.append(float(row[0])-float(temp))
               if float(row[0])-float(temp) < 4 :
                 ArrivalTime.append(float(row[0])-float(temp))
                 print (temp)
               temp=row[0]

           f.close()
           plt.figure(1)
           plt.plot(ArrivalTime)
           plt.xlabel('Arrived Packets')
           plt.ylabel('Inter Arrival Time Offset [second]')

           plt.show()