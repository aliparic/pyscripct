# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import time
import pandas as pd
import math

if __name__=="__main__":

    col=["blue", "green" , "red"]
    cc=["Reno", "Cubic", "BBR"]

    col_iter=0

    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/bbr',]

    paths = [   '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/reno',
                '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/cubic',
                '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/bbr',]



    for path in paths:
       counter=0
       thr_fairness=[]
       rtt_fairness = []
       ave_throughput = []
       ave_rtt=[]
       rtt_total = []
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           p=os.path.join(path, pcap_file)
           #print(p)

           command = "tshark -r " + p + " -2  -R  '(ip.dst == 130.243.27.222) && (tcp.stream>=0)' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > "+p+".csv"

           command_rtt = "tshark -r " + p + " -2  -R  '(ip.src == 130.243.27.222) && (tcp.stream>=0) && (tcp.analysis.ack_rtt>0)' -T fields -e tcp.stream -e tcp.analysis.ack_rtt -E separator=, > "+p+"RTT.csv"

           #print("I am running the command")
           #os.system(command)
           #os.system(command_rtt)

           df = pd.read_csv(p+".csv", names=['stream', 'time', 'seq'])
           df_rtt = pd.read_csv(p+"RTT.csv", names=['stream', 'rtt'])
           stream=pd.unique(df.iloc[:,0])
           for level in stream:
               #print(pd.unique(df.iloc[:,0]))
               df_s = df.loc[df.stream == level]
               df_rtt_level = df_rtt.loc[df_rtt.stream == level]
               #print(df_s)

               df_2=df_s.sub(df_s.iloc[0,1], axis=1)

               df_tmp = df_2.sort_index(ascending=False)  # reverse the data frame to get the last row

               ave_throughput.append(df_tmp.iloc[0,2]/1000000/df_tmp.iloc[0,1])

               ave_rtt.append(df_rtt_level['rtt'].mean())

           #print(ave_throughput)
           #print(ave_rtt)
           #print(np.power(sum(ave_throughput), 2) / sum(np.power(np.asarray(ave_throughput), 2)) / 5)
           #print(np.power(sum(ave_rtt), 2) / sum(np.power(np.asarray(ave_rtt), 2)) / 5)

           thr_fairness.append(np.power(sum(ave_throughput),2)/sum(np.power(np.asarray(ave_throughput),2))/len(stream))
           #if (np.power(sum(ave_throughput),2)/sum(np.power(np.asarray(ave_throughput),2))/len(stream)) < .89:
           #     print(pcap_file, np.power(sum(ave_throughput),2)/sum(np.power(np.asarray(ave_throughput),2))/len(stream))
           rtt_fairness.append(np.power(sum(ave_rtt), 2) / sum(np.power(np.asarray(ave_rtt), 2)) / len(stream))
           ave_throughput=[]
           ave_rtt=[]


       #print(thr_fairness)
       #print(rtt_fairness)
       thr_out_frame=pd.DataFrame(thr_fairness)
       thr_out_frame.to_csv(path+"_thr_Fairness_1.csv",index=False, header=False)
       rtt_out_frame = pd.DataFrame(rtt_fairness)
       rtt_out_frame.to_csv(path+"_rtt_Fairness_1.csv", index=False, header=False)
       plt.figure(1)
       plt.plot(thr_fairness, color=col[col_iter])
       plt.plot(rtt_fairness,'--', color=col[col_iter])
       col_iter=col_iter+1
       thr_fairness=[]
       rtt_fairness=[]
       del  thr_out_frame, rtt_out_frame


    plt.show()


