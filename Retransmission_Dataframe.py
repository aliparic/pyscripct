# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import time
import pandas as pd

if __name__=="__main__":

    col=["blue", "green" , "red"]
    cc=["Reno","Cubic","BBR"]
    col_iter=0

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr']

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/bbr',]

  # pcaps located on my external storage





    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/bbr',]


    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/bbr',]

    df_result = pd.DataFrame(columns=['retrans'])


    for path in paths:
       retrans_percent = []
       counter=0
       percent=[]
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):

           p=os.path.join(path, pcap_file)

           command_retrans = "tshark -r " + p + " -2  -R  '(ip.dst == 130.243.27.222) && (tcp.stream>=0) && tcp.analysis.retransmission' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > "+p+"_retrans.csv"
           command_trans = "tshark -r " + p + " -2  -R  '(ip.dst == 130.243.27.222) && (tcp.stream>=0) && !tcp.analysis.retransmission && !tcp.analysis.fast_retransmission' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > " + p + "_trans.csv"

           try:
               df_retrans = pd.read_csv(p + "_retrans.csv", names=['stream', 'time', 'seq'])
           except:
               #print("I am running the command")
               os.system(command_retrans)
               os.system(command_trans)
               df_retrans = pd.read_csv(p + "_retrans.csv", names=['stream', 'time', 'seq'])


           df_trans = pd.read_csv(p+"_trans.csv", names=['stream', 'time', 'seq'])
           percent=(len(df_retrans["stream"]) / len(df_trans["stream"])*100)    # counting the retransmission percentage according to the number of rows in each csv file
           if percent < 100:
             retrans_percent.append(percent)   # adding the percentage of each flow to the final csv file



       plt.figure(1)
       plt.plot(retrans_percent, '-o', markersize=3, color=col[col_iter], label=cc[col_iter])
       plt.xlabel('sample')
       plt.ylabel('retransmission percentage')
       df_retrans = pd.DataFrame(retrans_percent)
       df_retrans.to_csv(path + "Retransmission.csv", index=False, header=False)
       col_iter = col_iter + 1
       plt.show()




