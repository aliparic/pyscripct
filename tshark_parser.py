
import os
import subprocess
from multiprocessing import Process, Manager
import matplotlib.pyplot as plt
import numpy as np
import csv


if __name__=="__main__":

    #paths=['./rmbt/386/CubicTCP', './rmbt/498/CubicMobile/', './rmbt/423/CongestionWindow'] for Cubic Mobile
    # paths = ['./rmbt/498/', './rmbt/498/CongestionWindow/CubicWithoutCongestionWindow']  for stationary cubic
    paths = ['./rmbt/386/RenoTCP', './rmbt/412/CongestionWindow/reno'] # for mobile NewReno

    #paths = ['./rmbt/498/CongestionWindow/Reno_20171121-111552']
    paths = ['./rmbt/498/RenoStationary', './rmbt/498/CongestionWindow/Reno_20171121-111552']
    paths= ['./rmbt/498/BbrStationary']
    #paths = ['./rmbt/498/CubicStationary', './rmbt/498/CongestionWindow/CubicWithoutCongestionWindow' ]

    paths=['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile384/bbr']

    for path in paths:
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           print(pcap_file)
           p=os.path.join(path, pcap_file)

           command = "tshark -r " + p + " -2  -R  '(ip.src == 130.243.27.222) && (tcp.analysis.ack_rtt>0)' -T fields  -e tcp.analysis.ack_rtt  > out.csv"
           os.system(command)
           f = open('out.csv', "r")
           reader = csv.reader(f)
           rtt=[]
           for row in reader:
               print(row[0])
               x = float(row[0])
               rtt.append(x)
           plt.figure(1)
           plt.xlim([0, 8])
           print (rtt)
           sorted_ = np.sort(rtt)
           p = 1. * np.arange(len(rtt)) / (len(rtt) - 1)
           plt.plot(sorted_,p)
           plt.xlabel('RTT Cubic Stationary')
           plt.ylabel('CDF')
           f.close()

    plt.show()