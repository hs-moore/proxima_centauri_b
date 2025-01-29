import pandas as pd
import numpy as np

def get_solar(z):
    if z > np.pi/2:
        s = 0
    else:
        s = q2*np.cos(z)
    return s

def get_albedo(tij):
    a = 0.525 - 0.245*np.tanh((tij - 268)/5)
    if a > 0.77:
        a = 0.77
    elif a < 0.28:
        a = 0.28
    return a

def get_infra(tij):
    sigma = 5.67e-8
    i = (sigma * tij**4)/(1 + 0.5925*(tij/273)**3)
    return i

def get_cheat(tij, f_ocean):
    if tij < 273:
        f_ice = 1 - np.exp((tij-273)/10)
        if tij > 263:
            c_ice = 9.2*c_land
        else:
            c_ice = 2*c_land
    else:
        f_ice = 0
        c_ice = 0
    c = (1-f_ocean)*c_land + f_ocean*((1-f_ice)*c_ocean + f_ice*c_ice)
    return c

#constants#
c_land = 5.25e6
c_ocean = 40*c_land
g = 6.67e-11
a = 0.04856*1.5e11
q = (0.00155*382.8e24)/(4*np.pi*a**2)
q2 = (0.00155*1360)/(0.04856**2)
period = 11.1868*86400
#diff = 5.394e-1 * 11.1868**(-2)
diff = 0.02 * 11.1868**(-1)
#diff = ((1/11.1868)*4.30130890052356*-1 + 1.78111335078534)#*(1/11.1868)
diff = 30*diff
print(diff)

def run(lon_step, time_step, n_days, fo):

    #initialise
    times = np.arange(start=0, stop=n_days, step=time_step)
    lon_deg = np.arange(start=2.5, stop=177.5+lon_step, step=lon_step)
    lon_rad = [x*np.pi/180 for x in lon_deg]
    lon_stp_rad = lon_step*np.pi/180

    temperature = np.zeros((len(lon_rad), len(times)))
    temperature[:, 0] = 350

    #run through time
    for i in range(0, len(times)-1):
        for j in range(0, len(lon_rad)):
            tij = temperature[j, i]
            lon = lon_rad[j]

            solar = get_solar(lon)
            albedo = get_albedo(tij)
            infra = get_infra(tij)
            c_heat = get_cheat(tij, fo)

            if j==len(lon_rad)-1: #longitude +90
                first_deriv = 0
                second_deriv = -(tij - temperature[j-1, i])/(lon_stp_rad**2)
            elif j==0: #longitude -90
                first_deriv = 0
                second_deriv = (temperature[j+1, i] - tij)/(lon_stp_rad**2)
            else:
                first_deriv = (temperature[j+1, i] - temperature[j-1, i])/(2*lon_stp_rad)
                second_deriv = (temperature[j+1, i] - 2*tij + temperature[j-1, i])/(lon_stp_rad**2)

            if np.tan(lon) == 0:
                term = 0
            else:
                term = diff*first_deriv/np.tan(lon)
            x = (solar*(1-albedo) + term + diff*second_deriv - infra)/c_heat
            temperature[j, i+1] = tij + x*time_step*period

    return temperature

time_step = 0.5
n_days = 1000
lon_step = 5
fo = 0.7

r = run(lon_step, time_step, n_days, fo)
df = pd.DataFrame(r)
filename = "diff_30.csv"
df.to_csv(filename)

