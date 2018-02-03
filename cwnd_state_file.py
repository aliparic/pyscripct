import time
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n >= 1:
        start = haystack.find(needle, start + 1)
        n -= 1
    return start

if __name__=="__main__":
 path = "/Users/aliparic/Desktop/scripts/logs/log-mobile_20180124/rmbt/498/fake.nodeid_MONROE.EXP.RMBT_2_1512148260.77_STATS"
 cwnd=[]
 with open (path, 'rt') as in_file:
     for line in in_file:
       i = 1
       while i < line.count("tcpi_snd_cwnd"):
          pos = find_nth(line, "tcpi_snd_cwnd", i)
          tmp=line[pos + 15:pos + 20]
          i=i+1
          cwnd.append(int(tmp[:tmp.find(",")]))
       print(cwnd)