import numpy as np
import matplotlib.pyplot as plt

def solar1(z):
    if z > np.pi/2:
        s = 0
    else:
        s = q2*np.cos(z)
    return s

def solar2(sz, j):
    s = sz*(1-np.exp(-1*tau))*j*sa_frac
    return s

q2 = (0.00155*1360)/(0.04856**2)
lon_step = 5
lon_deg = np.arange(start=2.5, stop=177.5+lon_step, step=lon_step)
lon_rad = [x*np.pi/180 for x in lon_deg]
lon_stp_rad = lon_step*np.pi/180
rp = 1*6371e3

side_area = 0.5*np.pi*(rp+50e3)**2 + 0.5*np.pi*rp**2
top_area = 4*np.pi*(rp+50e3)**2 * (lon_stp_rad/2*np.pi)
total_area = top_area + 2*side_area
sa_frac = side_area/total_area

tau = 1
s0 = [solar1(z) for z in lon_rad]

j = 1

for t in range(0, 100):
    ss = [solar2(sz, j) for sz in s0]
    si = [sz*np.exp(-1*tau) for sz in s0]

    stotal = []
    for i in range(0, len(lon_rad)):
        s = 0
        if i == 0:
            s = si[i] + 2*ss[i+1]
        elif i == len(lon_rad)-1:
            s = si[i] + 2*ss[i-1]
        else:
            s = si[i] + ss[i-1] + ss[i+1]
        stotal.append(s)
        if i > 17:
            s0[i] = s
    
plt.plot(stotal, color='blue', label='Final')
plt.plot(si, color='red', label='Unscattered')
plt.plot(ss, color='green', label='Scattered')
plt.plot(s0, color='black', label='Incident')
plt.xlabel('Longitude')
plt.ylabel('Solar flux')
plt.legend()
plt.show()