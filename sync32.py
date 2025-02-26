import numpy as np
import matplotlib.pyplot as plt

q2 = (0.00155*1360)/(0.04856**2)

lon_step = 5
lon_deg = np.arange(start=0, stop=360+lon_step, step=lon_step)
lon_rad = [x*np.pi/180 for x in lon_deg]
lon_stp_rad = lon_step*np.pi/180

rp = 1.1*6371e3

time_step = 1
period = 11.1868
e = 0.3

arr = np.zeros((len(lon_rad), 48))

for i in range(0, len(lon_rad)):

    for t in range(0, 48, time_step):
        m_anom = (2*np.pi*t)/period
        v = m_anom + (2*e + (e**3)/4)*np.sin(m_anom) + (5/4)*(e**2)*np.sin(2*m_anom) + (13/12)*(e**3)*np.sin(3*m_anom)
        s_toa = q2 * ((1 + e*np.cos(v))/(1-e**2))**2
        omega = lon_rad[i] + np.pi*((2*t)/(2*period) -1)
        s = s_toa*np.cos(omega)
        if s < 0:
            s = 0
        arr[i, t] = s

c = plt.pcolormesh(arr, cmap='jet')
plt.colorbar(c, label='Solar flux ($W m^{-2}$)')
plt.xlabel('Time (days)')
plt.ylabel('Longitude')
plt.show()