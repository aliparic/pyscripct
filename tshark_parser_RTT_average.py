# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import pandas as pd

if __name__=="__main__":


    #paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile384/reno',
    #         '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile384/cubic',
    #         '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile384/bbr']

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/bbr']

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr']

    for path in paths:
       rtt = []
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
               str.append(int(row[1]))
           stream=[item for item, count in collections.Counter(str).items() if count > 1]
           #print (stream)
           f.close()
           for st in stream:
               f = open('out.csv', 'rt')
               reader = csv.reader(f)
               for row in reader:
                      if int(row[1]) == st:
                         rtt.append(float(row[0]))
               f.close()

       df = pd.DataFrame(rtt)
       df.to_csv(path+".csv", header=None)

       plt.figure(1)
       plt.xlim([0, 8])
       print (rtt)
       sorted_ = np.sort(rtt)
       p = 1. * np.arange(len(rtt)) / (len(rtt) - 1)
       plt.plot(sorted_, p)
       plt.xlabel('RTT Stationary')
       plt.ylabel('CDF')
       plt.show()


