# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import time
import pandas as pd

if __name__=="__main__":
    transmission_time=17
    col=["blue", "green" , "red"]
    cc=["Reno","Cubic","BBR"]
    col_iter=0



  # pcaps located on my external hard disks



    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/bbr',]

    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/bbr',]



    for path in paths:
       df_result = pd.DataFrame(columns=['group', 'rtt', 'thr'])
       counter=0
       rtt_3whs = []
       rtt_total = []
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           #print("started")
           #print(pcap_file)
           p=os.path.join(path, pcap_file)
           print(pcap_file)

           command_syn_rtt = "tshark -r " + p + " -2  -R  '(ip.src == 130.243.27.222 and tcp.flags.syn == 1 && tcp.flags.ack==1)' -T fields -e tcp.stream -e tcp.analysis.ack_rtt -E separator=, > "+p+"_3WHS_RTT.csv"


          # try:

          #      df = pd.read_csv(p + "_3WHS_RTT.csv", names=['stream', 'rtt'])

        #   except:
           os.system(command_syn_rtt)
           df = pd.read_csv(p + "_3WHS_RTT.csv", names=['stream', 'rtt'])

           for level in pd.unique(df.iloc[:,0]):
               df_3whs = df.loc[df.stream == level]
               print(df_3whs)
               df_rtt_level = df_3whs.loc[df_3whs.stream == level]

               #ave_throughput.append(df_tmp.iloc[0,2]/1000000/(df_tmp.iloc[0,1]-8))
               if df_rtt_level['rtt'].mean()<3:
                   rtt_3whs.append(df_rtt_level['rtt'].mean() *1000)
                   print(rtt_3whs)


       plt.figure(1)
       plt.plot(rtt_3whs , 'o', markersize=3, color=col[col_iter], label=cc[col_iter])
       plt.legend()
       plt.ylabel('Ave. 3WHS RTT [msec]')
       plt.xlabel('samples')
       col_iter = col_iter + 1
       df_result=pd.DataFrame(np.array(rtt_3whs))
       df_result.to_csv(path+"_3WHS_RTT_.csv", index = False, header = False)
       rtt_3whs=[]
       del(df_result)


    plt.show()


