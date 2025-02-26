import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

files = ['s32_e0.3', 'toa_p10']
lg = ['3:2', '1:1']

diffs = []
fig, (ax1) = plt.subplots(1, 1, sharey=True)

for i in range(0, len(files)):
    df = pd.read_csv('' + str(files[i]) + '.csv')
    temperature = df.to_numpy()
    temperature = temperature[:, 1:]
    temp = temperature[:, -1]
    if i == 1:
        temp2 = [*temp[::-1] , *temp]
        #print(np.max(temp2), np.min(temp2))`
        diffs.append(temp2)
    else:
        diffs.append(temp)

(lons, n_times) = temperature.shape
lon_step = int(180/(lons-1))
lons_rad = np.arange(start=0+lon_step/2, stop=360+lon_step/2, step=lon_step)



for i in range(0, len(diffs)):
    #if i <= 2:
    ax1.plot(lons_rad, diffs[i], label=lg[i])
    #elif i <= 5:
    #    ax2.plot(lons_rad, diffs[i], label=lg[i-3])
    #else:
    #    ax3.plot(lons_rad, diffs[i], label=lg[i-6])

ax1.plot([0, 360], [273, 273], ls='dashed', color='black')
ax1.plot([0, 360], [453, 453], ls='dashed', color='black')#453 for 10 bar
#ax2.plot([-180, 180], [273, 273], ls='dashed', color='black')
#ax2.plot([-180, 180], [494, 494], ls='dashed', color='black')
#ax3.plot([-180, 180], [273, 273], ls='dashed', color='black')
#ax3.plot([-180, 180], [574, 574], ls='dashed', color='black')
fig.supxlabel('Longitude ($\circ$)')
fig.supylabel('Temperature ($K$)')
ax1.legend()
#ax2.legend()
#ax3.legend()
fig.suptitle('10 bar, $CO_2$ atmosphere')
#ax1.set_title('10 bar')
#ax2.set_title('25 bar')
#ax3.set_title('100 bar')
#fig.set_figwidth(12)
#plt.plot([90, lons/2], [min(temp), max(temp)], ls='dashed', color='black')
plt.savefig('sync_comp.png')
plt.show()