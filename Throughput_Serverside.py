# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections

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
             '/Volumes/Untitled/ServerLog_Stationary2/Stationary/']

    for path in paths:
       ave_throughput = []
       rtt_total = []
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           print(pcap_file)
           p=os.path.join(path, pcap_file)
           command = "tshark -r " + p + " -2  -R  '(ip.src == 46.194.205.245) && (ip.dst == 130.243.27.222) && (tcp.stream>=0)' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > ./out.csv"
           os.system(command)
           f = open('out.csv', "r")
           reader = csv.reader(f)
           str=[]
           for row in reader:
               print(row)
               str.append(int(row[0]))
           stream=[item for item, count in collections.Counter(str).items() if count > 1]
           f.close()
           print (stream)
           rtt = []
           for st in stream:
               f = open('out.csv', "r")
               reader = csv.reader(f)
               first_row = next(reader)
               tmp = 0
               print (st)
               tmp=0
               for row in reader:
                      if int(row[0]) == st:
                            if int(row[2])< tmp:
                                break
                            tmp=int(row[2])
               thr_ave= round((tmp/1024)/float(row[1]),2)
               ave_throughput.append(thr_ave)
               print(ave_throughput)
               f.close()
       plt.figure(1)
       sorted_ = np.sort(ave_throughput)
       p = 1. * np.arange(len(ave_throughput)) / (len(ave_throughput) - 1)
       plt.plot(sorted_,p,'.', markersize=.1, color=col[col_iter])
       plt.plot(sorted_, p, color=col[col_iter])
       print ("printed in:", col[col_iter])
       col_iter=col_iter+1
       plt.ylabel('CDF')
    plt.show()


