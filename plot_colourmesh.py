import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('optical0.1_1re_co2_p10_d1_i.csv')
temperature = df.to_numpy()
temperature = temperature[:, 1:]
(lons, n_times) = temperature.shape
lon_step = int(180/(lons-1))
print(lons, lon_step)

c = plt.pcolormesh(temperature, cmap='jet')
plt.colorbar(c, label='Temperature ($K$)')
plt.show()

temp = temperature[:, -1]
lons_rad = np.arange(start=-180+lon_step/2, stop=180+lon_step/2, step=lon_step)
temp2 = [*temp[::-1] , *temp]
print(temp2)
plt.plot(lons_rad, temp2)
plt.plot([-180, 180], [273, 273], ls='dashed', color='black')
plt.plot([-180, 180], [373, 373], ls='dashed', color='black')
plt.xlabel('Longitude ($\circ$)')
plt.ylabel('Temperatuer ($K$)')
#plt.plot([90, lons/2], [min(temp), max(temp)], ls='dashed', color='black')
plt.show()