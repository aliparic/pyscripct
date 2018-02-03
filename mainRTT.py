import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv("ping412.csv")
#saved_column=df['The RTT to ACK the segment was']
saved_column=df['Response time']

plt.figure(1)
plt.plot(saved_column)
plt.title('RTT in Uplink Transmission')
plt.xlabel('samples')
plt.ylabel('RTT [second]')


plt.figure(2)
plt.xlim([40, 200])
sorted_ = np.sort(saved_column)
yvals = np.arange(len(sorted_)) / float(len(sorted_))
plt.plot(sorted_, yvals , label = 'uplink')
plt.title('RTT in Uplink Transmission')
plt.xlabel('round trip time [ms!]')
plt.ylabel('CDF')
plt.show()


