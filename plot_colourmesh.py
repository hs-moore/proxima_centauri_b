import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('s32_e0.4.csv')
temperature = df.to_numpy()
temperature = temperature[:, 1:]
(lons, n_times) = temperature.shape
lon_step = int(360/(lons-1))
print(lons, lon_step)

c = plt.pcolormesh(temperature, cmap='jet')
plt.colorbar(c, label='Temperature ($K$)')
plt.show()

temp = temperature[:, -1]
lons_rad = np.arange(start=0+lon_step/2, stop=360+lon_step/2, step=lon_step)
#temp2 = [*temp[::-1] , *temp]
#print(temp2)
plt.plot(lons_rad, temp)
plt.plot([0, 360], [273, 273], ls='dashed', color='black')
plt.plot([0, 360], [453, 453], ls='dashed', color='black')
plt.xlabel('Longitude ($\circ$)')
plt.ylabel('Temperatuer ($K$)')
#plt.plot([90, lons/2], [min(temp), max(temp)], ls='dashed', color='black')
plt.show()