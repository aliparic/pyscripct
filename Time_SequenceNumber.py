
import os
import subprocess
from multiprocessing import Process, Manager
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

if __name__=="__main__":

    #paths=['./rmbt/386/CubicTCP', './rmbt/498/CubicMobile/', './rmbt/423/CongestionWindow'] for Cubic Mobile
    # paths = ['./rmbt/498/', './rmbt/498/CongestionWindow/CubicWithoutCongestionWindow']  for stationary cubic
    paths = ['./rmbt/386/RenoTCP', './rmbt/412/CongestionWindow/reno'] # for mobile NewReno

    #paths = ['./rmbt/498/CongestionWindow/Reno_20171121-111552']
    paths = ['./rmbt/498/RenoStationary', './rmbt/498/CongestionWindow/Reno_20171121-111552']
    #paths = ['./rmbt/498/CubicStationary', './rmbt/498/CongestionWindow/CubicWithoutCongestionWindow' ]

    #paths = [
        # '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180123/rmbt/498/CongestionWindow/CubicWithoutCongestionWindow',
        #'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/bbrMobile']  # for stationary cubic


    #paths = [#'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno',
             #'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
             #'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr']

    paths = [#'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno/TS',]
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic/TS',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/bbr/TS']

    for path in paths:
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           print(pcap_file)
           p=os.path.join(path, pcap_file)

           #command = "tshark -r " + p + " -2  -R  '(ip.dst == 130.243.27.222) && (ip.src==46.194.104.156)' -T fields  -e tcp.seq -e frame.time_epoch -E separator=, > out.csv"
           command = "tshark -r " + p + " -2  -R  '(ip.dst == 130.243.27.222) && (tcp.analysis.ack_rtt>0) ' -T fields  -e tcp.seq -e frame.time_epoch -E separator=, > out.csv"
           command = "tshark -r " + p + " -2  -R  '(tcp.stream == 4) && (tcp.analysis.ack_rtt>0) && (ip.dst == 46.194.205.245) && (ip.src == 130.243.27.222)' -T fields  -e tcp.seq -e frame.time_epoch -E separator=, > out.csv"
           #command = "tshark -r " + p + " -2  -R  '(tcp.stream == 3) && (tcp.analysis.ack_rtt>0) && (ip.dst == 46.194.205.245) && (ip.src == 130.243.27.222)' -T fields  -e tcp.analysis.ack_rtt -e frame.time_epoch -E separator=, > out.csv"

           os.system(command)
           f = open('out.csv', "r")
           reader = csv.reader(f)
           first_row = next(reader)
           start_time=float(first_row[1])
           seq=[]
           time=[]
           for row in reader:
               seq.append(float(row[0]))
               time.append(float(row[1])-start_time)
           print(time,seq)
           df = pd.DataFrame(time,seq)
           df.to_csv(p + "_rtt.csv", header=None)

           plt.figure(1)
           plt.plot(time,seq,'.', markersize=.8)
           plt.ylim(0, 30000000)
           plt.xlabel('Time')
           plt.ylabel('Sequence Number')
           f.close()
       plt.show()

