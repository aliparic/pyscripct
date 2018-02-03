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

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/bbr']

    for path in paths:
       rtt_total = []
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           print(pcap_file)
           p=os.path.join(path, pcap_file)

           command = "tshark -r " + p + " -2  -R  '(ip.src == 130.243.27.222) && (tcp.analysis.ack_rtt>0)' -T fields  -e tcp.analysis.ack_rtt -e tcp.stream -E separator=, > out.csv"
           os.system(command)
           f = open('out.csv', "r")
           reader = csv.reader(f)
           str=[]
           for row in reader:
               #print (row)
               str.append(int(row[1]))
           stream=[item for item, count in collections.Counter(str).items() if count > 1]
           #print (stream)
           f.close()
           rtt = []
           for st in stream:
               f = open('out.csv', 'rt')
               reader = csv.reader(f)
               print (st)
               for row in reader:
                      if int(row[1]) == st:
                         rtt.append(float(row[0]))
                         rtt_total.append(float(row[0]))
               plt.figure(1)
               plt.xlim([0, 8])
               sorted_ = np.sort(rtt)
               p = 1. * np.arange(len(rtt)) / (len(rtt) - 1)
               plt.plot(sorted_,p,'.', markersize=.1, color=col[col_iter])
               print ("printed in:", col[col_iter])
               plt.ylabel('CDF')
               f.close()
               rtt = []

       sorted_ = np.sort(rtt_total)
       p = 1. * np.arange(len(rtt_total)) / (len(rtt_total) - 1)
       plt.plot(sorted_, p, linewidth=4, color=col[col_iter])
       col_iter = col_iter + 1
       rtt_total=[]
    plt.show()


