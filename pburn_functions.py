# CSE 6730 Project 2
# Sooji Ha
import math
from math import pi
from readData import readData
import fire_states as fs

# Defining constants from Alexandridis et al. (2008)
c1  = 0.045
c2  = 0.131
a   = 0.078
p_h = 0.58
pDen_1 = -0.4
pDen_2 = 0
pDen_3 = 0.3 

# Cell Size
l = 30     

# Defining fire directions
fire_rad = [0, pi/4, pi/2, (3*pi)/4, pi, (5*pi)/4, (3*pi)/2, (7*pi)/4]

# Reading data files
data = readData()

# Calculates burn probability from cell (i,j) to cell (m,n)
def p_burn(i, j, m, n):
    
    # Probability from Vegetation Density
    density = data['EVC'][m,n]
    if density < 0.33:
        p_den = pDen_1
    elif density < 0.67:
        p_den = pDen_2
    else:
        p_den = pDen_3

    # Probability from Vegetation Type
    if data['EVT'][m,n] == 1:
        p_veg = -0.3
    elif data['EVT'][m,n] == 2:
        p_veg = 0
    elif data['EVT'][m,n] == 3:
        p_veg = 0.4
    else:
        p_veg = 0
        
    # Probability from Wind Direction & Velocity
    V = fs.V
    fire_direction = fire_rad[fs.det_neighborID(i,j,m,n)]
    theta_p = fs.wind_direction - fire_direction
    f_t = math.exp(V*c2*(math.cos(theta_p)-1))
    p_w = math.exp(c1*V)*f_t
    
    # Probability from Slope
    E1 = data['DEM'][i,j] # center cell elevation
    E2 = data['DEM'][m,n] # neighboring cell elevation
    if fs.det_neighborID(i,j,m,n) % 2 == 1:
        theta_s = math.atan(abs(E1 - E2) / (l * math.sqrt(2)))
    else:
        theta_s = math.atan(abs(E1 - E2) / l)
    p_s = math.exp(a*theta_s)
    
    # Final Burn Probability
    p_b=p_h*(1+p_veg)*(1+p_den)*p_w*p_s
    
    return p_b
