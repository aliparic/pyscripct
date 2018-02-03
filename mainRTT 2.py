import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv("RTT386RMBT.csv")
saved_column=df['The RTT to ACK the segment was']
#saved_column=df['Response time']/1000

plt.figure(1)



plt.xlim([0, 11])
sorted_ = np.sort(saved_column)
yvals = np.arange(len(sorted_)) / float(len(sorted_))
plt.plot(sorted_, yvals , label = 'uplink')
plt.title('RTT in Uplink Transmission')
plt.xlabel('round trip time [seconds!]')
plt.ylabel('CDF')
plt.show()


'''

plt.plot(saved_column)
plt.title('RTT in Uplink Transmission')
plt.xlabel('samples')
plt.ylabel('RTT [second]')
plt.show()





plt.plot(saved_column)
plt.title('RTT in Uplink Transmission')
plt.xlabel('sample')
plt.ylabel('RTT[second]')
plt.show()

'''