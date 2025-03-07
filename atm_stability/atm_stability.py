import numpy as np
import matplotlib.pyplot as plt

albedo = [0, 0.5, 0.9]
mu = [1, 10, 100]
pressure = [0.001, 0.01, 0.1, 1, 10, 100]

sep = 0.04856*1.5e11
ndof = 5
sb_const = 5.67e-8
gas_const = 8314
kb_const = 1.38e-23
m_H = 1.67e-27
T_star = 2900
R_star = 0.141*695700e3
M_star = 0.1221*1.99e30
m_p = 1.07*5.972e24#10*5.972e24# #lower/upper bound
r_p = 1*6371e3 #assumed value
G_const = 6.67e-11

bond_a = 0 #take bond albedo to be 0

grav = (G_const * m_p)/(r_p**2)
density = (3 * m_p)/(4*np.pi*r_p**3)

#2.1 stellar irradiation and orbtial prameter

T_irr = T_star*(R_star/sep)**(1/2)*(1-bond_a)**(1/4)
flux = sb_const*T_irr**4 # at substellar point
rot_freq = (G_const*M_star/sep**3)*(1/2)

#2.2 

gamma = 1+2/ndof

colors = ['blue', 'magenta', 'green']
i=0
#for a in albedo:
#    T_irr = T_star*(R_star/sep)**(1/2)*(1-a)**(1/4)
#
#    lim = []
#    for p in pressure:
#        frac1 = (gamma*kb_const*T_irr/m_H)**(1/2)
#        frac2 = ((2+ndof)*gas_const*p)/(2*sb_const*grav*r_p)
#        mu_lim = (frac1*frac2*(T_star**(-3))*(R_star**(-3/2))*((1-a)**(-3/4))*(sep**(3/2)))**(2/3)
#        lim.append(mu_lim)

#    plt.plot(pressure, lim, color=colors[i])
#    plt.fill_betweenx(lim, pressure, facecolor=colors[i], alpha=0.2, edgecolor=colors[i])
#    i+=1
    
#plt.xlim((0.57, 10))
#plt.ylim((1, lim[-2]))
#plt.xscale('log')
#plt.xticks(ticks=[1, 10], labels=[1, 10])
#plt.xlabel('Pressure ($bar$)')
#plt.ylabel('$\mu$')
#plt.text(3.5, 1.25, 'Stable Atmospheres')
#plt.savefig('stable_atm.png')
#plt.show()

#print(lim[-2])
