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


 paths = [
          #"/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/bbrStationary"
           '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile384/bbr',
           '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile384/cubic',
           '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile384/reno']


 paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno/TS/',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic/TS',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr/TS']

 paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/reno/TS',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/cubic/TS',
          '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/stationary/stationary2/bbr/TS']


 for index, path in enumerate(paths):
     print(path)
     files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('txt')]
     print(files)
     for index, file in enumerate(files):
         p = os.path.join(path, file)
         #print(p)
         with open (p, 'rt') as in_file:
             cwnd = []
             tmp_cwnd = []
             for line in in_file:
               wordlist = re.sub("[^\w]", " ", line).split()
               count=1
               tmp_cwnd = []
               while count < len(wordlist):
                   if wordlist[count]=="cwnd":
                       tmp_cwnd.append(int(wordlist[count+1]))
          #             print (tmp_cwnd)
                       #count=count+1
                   count=count+1
               if len(tmp_cwnd)==5:
                   cwnd.append(tmp_cwnd)
         #print (cwnd)
             plt.figure(1)
             print("figure is going to be ploted")
             for i in range(0,4):
                cwnd_ = [item[i] for item in cwnd]
                print(cwnd_)
                plt.plot(cwnd_)
             plt.xlabel('Sample')
             plt.ylabel('CWND')
             plt.ylim(0, 1000)
             plt.show()
