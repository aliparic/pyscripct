
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import subprocess


if __name__=="__main__":

    #paths=['./rmbt/386/CubicTCP', './rmbt/498/CubicMobile/', './rmbt/423/CongestionWindow'] for Cubic Mobile

    paths = ['/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/reno',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/cubic',
             '/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/mobile/mobile386/bbr']
    average_ret = []
    for path in paths:
       retransmit=[]
       retrans_percent=[]
       tcp=[]
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           #print(pcap_file)
           p=os.path.join(path, pcap_file)
           filter_tcp="(ip.dst == 130.243.27.222 && tcp) && !(tcp.analysis.out_of_order) && !(tcp.analysis.retransmission) && !(tcp.analysis.fast_retransmission) && !(tcp.analysis.duplicate_ack)"
           filter_ret="(tcp.analysis.fast_retransmission || tcp.analysis.retransmission) && ip.dst == 130.243.27.222"
           #filter_ret='tcp.analysis.retransmission'

           #cmd = "tshark -r " + p + " -2  -R  '(tcp.analysis.fast_retransmission || tcp.analysis.retransmission) && ip.dst == 130.243.27.222'  | wc -l"

           cmd = "tshark -r " + p + " -2  -R '" + filter_ret + "' | wc -l"
           proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
           (out, err) = proc.communicate()
           retransmit = ([int(s) for s in out.split() if s.isdigit()])
           cmd = "tshark -r " + p + " -2  -R '" + filter_tcp + "' | wc -l"
           proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
           (out, err) = proc.communicate()
           tcp =([int(s) for s in out.split() if s.isdigit()])
           retrans_percent.append(round(retransmit[0]/tcp[0],2))
           print(retrans_percent)

       average_ret.append(sum(retrans_percent)/len(retrans_percent)*100)
       print(average_ret)









