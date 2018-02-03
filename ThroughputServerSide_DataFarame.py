# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import pandas as pd

if __name__=="__main__":

    col=["blue", "green" , "red"]
    col_iter=0
    #paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary5_poor_cache_reset/reno',
    #         '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary5_poor_cache_reset/cubic',
    #         '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary5_poor_cache_reset/bbr']

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr']

    paths = [#'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno',
             #'/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic',
             #'/Volumes/Untitled/ServerLog_Stationary2/Stationary/']
             '/Volumes/Untitled/ServerLog_Stationary2/Mobile386/']

    for path in paths:
       ave_throughput = []
       rtt_total = []
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           print("started")
           print(pcap_file)
           p=os.path.join(path, pcap_file)

           command = "tshark -r " + p + " -2  -R  '(ip.src == 46.194.205.245) && (ip.dst == 130.243.27.222) && (tcp.stream>=0)' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > ./out.csv"
           #tshak command for mobile386 pcaps
           command = "tshark -r " + p + " -2  -R  '(ip.src == 46.194.79.121) && (ip.dst == 130.243.27.222) && (tcp.stream>=0)' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > ./out.csv"

           #os.system(command)
           f = open('out.csv', "r")
           reader = csv.reader(f)
           df=pd.read_csv("out.csv",names = ['stream', 'time', 'seq'])
           #print(df)
           for level in pd.unique(df.iloc[:,0]):
               print(pd.unique(df.iloc[:,0]))
               df_s = df.loc[df.stream == level]
               print(df_s)
               plt.figure(1)
               #print(df_s.iloc[0,1])
               df_2=df_s.sub(df_s.iloc[0,1], axis=1)

               df_tmp = df_2.sort_index(ascending=False)  # reverse the data frame to get the last row

               if df_tmp.iloc[0,2]>1000000:   # filter the unnecessary data
                  plt.plot(df_2.time,df_s.seq,'.',markersize=.2)
               plt.ylim(0,40000000)
               #print("printed in:", col[col_iter])
               #col_iter = col_iter + 1
               #plt.ylabel('CDF')
           plt.show()



