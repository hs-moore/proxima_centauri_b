import pandas as pd
import numpy as np

def get_solar(z, q3):
    if z > np.pi/2:
        s = 0
    else:
        s = q2*np.cos(z)
        #s = q3/(90/lon_step)
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

def get_toa(tij, lon):

    u = np.cos(lon)
    p = pressure * pco2 * 10**(-6)
    a = get_albedo(tij)

    if tij < 190:
        tij = 190
    if tij > 370:
        tij = 370

    if tij < 280:
        toa = -0.6891 + 1.0468*a + 0.007845*tij -0.0028373*p -0.28899*u
        toa += -0.037412*a*p - 0.0063499*u*p + 0.20122*a*u
        toa += -0.0018508*a*tij + 0.00013649*u*tij + 9.8581e-5*p*tij
        toa += 0.073239*a**2 - 1.6555e-5*tij**2 + 6.5817e-4*p**2 + 0.081218*u**2

    else:
        toa = 1.1082 + 1.5172*a - 5.7993e-3*tij +0.019705*p - 0.1867*u
        toa += -0.031355*a*u - 0.010214*u*p + 0.20986*a*u
        toa += -3.7098e-3*a*tij -1.1335e-4*u*tij +5.3714e-5*p*tij 
        toa += 0.075887*a**2 +9.269e-6*tij**2 - 4.1327e-4*p**2 + 0.063298*u**2

    return toa

#########################################

def run(lon_step, time_step, n_days, fo, m0):

    #initialise
    times = np.arange(start=0, stop=n_days, step=time_step)
    lon_deg = np.arange(start=2.5, stop=177.5+lon_step, step=lon_step)
    lon_rad = [x*np.pi/180 for x in lon_deg]
    lon_stp_rad = lon_step*np.pi/180

    temperature = np.zeros((len(lon_rad), len(times)))
    temperature[:, 0] = 350

    q3 = 0
    for i in range(0, 18):
        q3 += q2 * np.cos(lon_rad[i])
    print(q2, q3)
    #run through time
    for i in range(0, len(times)-1):
        for j in range(0, len(lon_rad)):
            tij = temperature[j, i]
            lon = lon_rad[j]

            solar = get_solar(lon, q3)
            #albedo = get_albedo(tij)
            albedo = get_toa(tij, lon)
            infra = get_infra(tij)
            c_heat = get_cheat(tij, fo)

            t_avg = np.average(temperature[:, i])
            diff = 0.02 * pressure * 11.1868**(-1) * (m0/29)**2 * (t_avg/288)**12
            diff = d_mult*diff/t_adv

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

n2_cp = {100:[64.4, 56.3], 200:[30.4, 45.5], 300:[29.6, 33.4]}
co2_cp = {100:[37.1], 200:[37.1], 300:[37.2]}

time_step = 0.05
n_days = 250
lon_step = 5
fo = 0.7

#constants#
c_land = 5.25e6
c_ocean = 40*c_land
g = 6.67e-11
a = 0.04856*1.5e11
q = (0.00155*382.8e24)/(4*np.pi*a**2)
q2 = (0.00155*1360)/(0.04856**2)
period = 11.1868*86400
pressure = 10 #in bar
pco2 = 300 # in ppm
m0 = 44
d_mult = 1
#diff = ((1/11.1868)*4.30130890052356*-1 + 1.78111335078534)#*(1/11.1868)
rp = 0.5*6371e3
t_adv = (rp/1e3) / (time_step * period)
print(t_adv)
#
#print(diff)

r = run(lon_step, time_step, n_days, fo, m0)
df = pd.DataFrame(r)
filename = "tadv_0.5re_co2_p" + str(pressure) + '_d' + str(d_mult) + "_i.csv"
df.to_csv(filename)

