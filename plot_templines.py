import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

files = ['o0.1_re0.5', 'o0.1_re1', 'o0.1_re2', 'o1_re0.5', 'o1_re1', 'o1_re2']

diffs = []
for i in files:
    df = pd.read_csv('tadv_' + str(i) + '_i.csv')
    temperature = df.to_numpy()
    temperature = temperature[:, 1:]
    temp = temperature[:, -1]
    temp2 = [*temp[::-1] , *temp]
    print(np.max(temp2), np.min(temp2))
    diffs.append(temp2)

(lons, n_times) = temperature.shape
lon_step = int(180/(lons-1))
lons_rad = np.arange(start=-180+lon_step/2, stop=180+lon_step/2, step=lon_step)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

for i in range(0, len(diffs)):
    if i < len(files)/2:
        ax1.plot(lons_rad, diffs[i], label=files[i])
    else:
        ax2.plot(lons_rad, diffs[i], label=files[i])

ax1.plot([-180, 180], [273, 273], ls='dashed', color='black')
ax1.plot([-180, 180], [373, 373], ls='dashed', color='black')#453 for 10 bar
ax2.plot([-180, 180], [273, 273], ls='dashed', color='black')
ax2.plot([-180, 180], [373, 373], ls='dashed', color='black')
fig.supxlabel('Longitude ($\circ$)')
fig.supylabel('Temperature ($K$)')
ax1.legend()
ax2.legend()
#fig.suptitle('I/lons')
#plt.plot([90, lons/2], [min(temp), max(temp)], ls='dashed', color='black')
plt.savefig('tadv_o_temps_i.png')
plt.show()