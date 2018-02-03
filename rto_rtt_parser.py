import time
import re
import numpy as np
import matplotlib.pyplot as plt
import os


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n >= 1:
        start = haystack.find(needle, start + 1)
        n -= 1
    return start

if __name__=="__main__":


 paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile384/reno',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile384/cubic',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile384/bbr']
 #paths = [
 #          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr',
 #          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
 #          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno']

 paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/bbr']

 paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr']


 for index, path in enumerate(paths):
     #print(path)
     files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('txt')]
     #print(files)
     for index, file in enumerate(files):
         p = os.path.join(path, file)
         #print(p)
         with open (p, 'rt') as in_file:
             rto = []
             tmp_rto = []
             rtt=[]
             tmp_rtt = []
             difference = []
             for line in in_file:
               wordlist = re.sub("[^\w]", " ", line).split()
               count=1
               tmp_rto = []
               tmp_rtt = []
               while count < len(wordlist):
                   if wordlist[count]=="rto":
                       tmp_rto.append(int(wordlist[count+1]))
                       print(tmp_rto)
                   if wordlist[count]=="rtt":
                       tmp_rtt.append(int(wordlist[count+1]))
                       print(tmp_rtt)
                   count=count+1
               if len(tmp_rtt) and len (tmp_rto)==5:
                   rto.append(tmp_rto)
                   rtt.append(tmp_rtt)
                   #print(tmp_rto)
                   print(tmp_rto, tmp_rtt)
                   difference.append(np.subtract(tmp_rto, tmp_rtt))
         #print (rto)



         plt.figure(1)
         print("figure is going to be ploted")
         for i in range(0,4):
            dif_ = [item[i] for item in difference]
            plt.plot(dif_)
         plt.xlabel('Sample')
         plt.ylabel('RTO - RTT')
         plt.ylim(0, 15000)

         plt.figure(2)
         print("figure is going to be ploted")
         for i in range(0,4):
            rtt_ = [item[i] for item in rtt]
            plt.plot(rtt_)
         plt.xlabel('Sample')
         plt.ylabel('RTT')
         plt.ylim(0, 30000)

         plt.figure(3)
         print("figure is going to be ploted")
         for i in range(0,4):
            rto_ = [item[i] for item in rto]
            plt.plot(rto_)
         plt.xlabel('Sample')
         plt.ylabel('RTO')
         plt.ylim(0, 30000)
     plt.show()