import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

nums = [1, 10, 20, 30]

diffs = []
for i in nums:
    df = pd.read_csv('diff_' + str(i) + '.csv')
    temperature = df.to_numpy()
    temperature = temperature[:, 1:]
    temp = temperature[:, -1]
    temp2 = [*temp[::-1] , *temp]
    print(np.max(temp2), np.min(temp2))
    diffs.append(temp2)

(lons, n_times) = temperature.shape
lon_step = int(180/(lons-1))
lons_rad = np.arange(start=-180+lon_step/2, stop=180+lon_step/2, step=lon_step)

for i in range(0, len(diffs)):
    plt.plot(lons_rad, diffs[i], label=nums[i])

plt.plot([-180, 180], [273, 273], ls='dashed', color='black')
plt.plot([-180, 180], [373, 373], ls='dashed', color='black')
plt.xlabel('Longitude ($\circ$)')
plt.ylabel('Temperature ($K$)')
plt.legend()
#plt.plot([90, lons/2], [min(temp), max(temp)], ls='dashed', color='black')
plt.savefig('diffs_temps.png')
plt.show()