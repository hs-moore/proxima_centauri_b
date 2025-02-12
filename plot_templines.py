import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

files = ['1re_co2_p10_d1', '2re_co2_p10_d1', '0.5re_co2_p10_d1', '1re_co2_p10_d2', '2re_co2_p10_d2', '0.5re_co2_p10_d2']

diffs = []
for i in files:
    df = pd.read_csv('tadv_' + str(i) + '_ilons.csv')
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
    if i < 3:
        ax1.plot(lons_rad, diffs[i], label=files[i])
    else:
        ax2.plot(lons_rad, diffs[i], label=files[i])

ax1.plot([-180, 180], [273, 273], ls='dashed', color='black')
ax1.plot([-180, 180], [453, 453], ls='dashed', color='black')
ax2.plot([-180, 180], [273, 273], ls='dashed', color='black')
ax2.plot([-180, 180], [453, 453], ls='dashed', color='black')
fig.supxlabel('Longitude ($\circ$)')
fig.supylabel('Temperature ($K$)')
ax1.legend()
ax2.legend()
fig.suptitle('I/lons')
#plt.plot([90, lons/2], [min(temp), max(temp)], ls='dashed', color='black')
plt.savefig('tadv_d_temps_ilons.png')
plt.show()