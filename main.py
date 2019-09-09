import fire_states as fs
import matplotlib.pyplot as plt
from matplotlib import cm
from fire_states import data
import numpy as np

plot = True   # Set to True to generate plots

nrow = 813      #Number of rows
ncol = 689      #Number of columns
time_sim = 100  #Simulation time

# Initialize state array based on vegetation type
fs.init_states()

# Use Rough Ridge start position
i = 392
j = 321

# Initialize fire
fs.init_fire(i,j)

# Initialize state array
states = np.zeros([nrow,ncol,time_sim])

# Loop over time
print("Time\tCells Burning\tCells Burned Down")
for t in range(0,time_sim):
    
    # Update state
    states[:,:,t] = fs.update_states()
    
    # State statistics
    num_burning = np.sum(np.sum(states[:,:,t]==3))
    num_burned = np.sum(np.sum(states[:,:,t]==4))
    num_flammable = np.sum(np.sum(states[:,:,t]==2))
    print("%d\t%d\t\t%d" % (t, num_burning, num_burned))

# Plotting results
if plot:
    statesbinary = states.copy()
    statesbinary[statesbinary<4] = 0
    
    plt.close('all')
    plt.figure(1)
    plt.contourf(data["X"]/1000, data["Y"]/1000, data["DEM"])
    interval = 10
    statesum = np.sum(statesbinary[:,:,2:-1:interval],axis=2)
    plt.contour(data["X"]/1000, data["Y"]/1000, statesum,cmap=cm.jet) 
    plt.title('Fire Domain, Wind %.1f m/s @ %.1f Degrees' % (fs.V, -(fs.wind_direction - fs.pi) * 180/fs.pi))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('square')
    
    num_burned = np.zeros([time_sim,1])
   
    for i in range(0,time_sim):
        num_burned[i] = np.sum(np.sum(states[:,:,i]==4))
    
    plt.figure()
    plt.plot(range(0,time_sim),num_burned)
    plt.xlabel("Timestep")
    plt.ylabel("Number of cells")
    plt.title("Fire Growth")
    
    plt.figure()
    plt.plot(range(0,time_sim),num_burned)
    plt.xlabel("Timestep")
    plt.ylabel("Number of cells")
    plt.title("Fire Growth, Logarithmic Scale")
    plt.xscale("log")
    plt.yscale("log")
