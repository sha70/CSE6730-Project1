# CSE 6730 Project 2
# Felice Chan

import numpy as np
import random
import math
from math import pi
from pburn_functions import p_burn, data

# Baseline conditions
wind_direction = 0
V = 10 

# Map and Grid Dimensions
nrow = 813
ncol = 689
l = 30 

# Probability that a cell will catch fire due to spotting
pc0 = 0.1   

# Constants from Alexandridis et. al     
c1 = 0.045
c2 = 0.131
a = 0.078
p_h = 0.58

state_old = np.empty(shape=(nrow,ncol))
state_new = state_old.copy()
count2 = 0

# Initialize a 2d array for states based on EVT data
def init_states():
    global count2
    for i in range(nrow):
        for j in range(ncol):
            if data['EVT'][i,j] == 0:
                state_old[i,j] = 1
                state_new[i,j] = 1
            else:
                state_old[i,j] = 2
                state_new[i,j] = 2
                count2 +=1

# Initialize a fire at determined i,j location
def init_fire(i,j):
    global state_old
    state_old[i,j] = 3

# Loop over map to update cell states
def update_states():
    global state_old
    global state_new
    for i in range(nrow):
        for j in range(ncol):
            if state_old[i,j] == 3:
                state_new[i,j] = 4
                check_neighbors(i,j)
                calc_spotting(i,j)
    state_old = state_new.copy()
    return state_old

# Function to determine an neighbor ID
def det_neighborID(i,j,m,n):
    if m < i and n < j:
        neighbor_id = 7
    elif m < i and n == j:
        neighbor_id = 0
    elif m < i and n > j:
        neighbor_id = 1
    elif m == i and n > j:
        neighbor_id = 2
    elif m > i and n > j:
        neighbor_id = 3
    elif m > i and n == j:
        neighbor_id = 4
    elif m > i and n < j:
        neighbor_id = 5
    elif m == i and n < j:
        neighbor_id = 6
    return neighbor_id

# Check 8 neighbors of a cell
def check_neighbors(i,j):
    for m in (i-1, i, i+1):
        for n in (j-1, j, j+1):
            # Skip cells out of bounds and skip self
            if (m < 0 or m >= nrow or n < 0 or n >= ncol):
                continue
            if (m == i and n == j):
                continue
            if state_old[m,n] == 2:
                pburn = p_burn(i,j,m,n)
                rn = random.uniform(0, 1)
                if rn < pburn:
                    state_new[m,n] = 3

# Function to calculate spotting
def calc_spotting(i,j):
    mu = V/2
    sigma = V/2
    rn = np.random.normal(mu,sigma)

    # Random direction of flaming material travel
    rand_direction = random.uniform(0,2*pi)
    
    # theta_p is the wind direction - some random direction.
    theta_p = wind_direction - rand_direction
    
    # dp is the equation for calculating the distance 
    dp = rn*math.exp(V*c2*(math.cos(theta_p)-1))
    
    # Determine new x and y values. 
    x = round(dp*math.cos(rand_direction))
    y = round(dp*math.sin(rand_direction))

    pcd = data['EVC'][i,j]
    pc = pc0*(1+pcd)

    rn_pc = random.uniform(0, 1)
    
    # If spotting, then update state_new(i,j) = 3
    if pc > rn_pc and state_old[i,j] != 1 and state_old[i,j] != 4:
        new_i = i + x
        new_j = j + y
        if  (new_i > 0 and new_i < nrow and new_j > 0 and new_j < ncol):
            if state_old[new_i,new_j] == 2:
                state_new[new_i,new_j] = 3