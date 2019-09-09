CSE6730: Project 2
Travis Burrows
Felice Chan
Susie Ha

This project was written in Python 3 and requires numpy, matplotlib, random, math, and csv packages to be installed.

Files:
main.py                   - starts simulation, calls the functions defined in the other files
readData.py               - reads in the data from the .csv files
fire_states.py            - contains functions for progressing fire and vegetations states
pburn_functions.py        - calculates fire spread probability
data.csv                  - stores geographical data of the area
Veg_Density_Converted.csv - stores the translations for vegetation and density that are used in our computatio

Usage: 
python3 main.py

Notes:
- To generate plots, run main.py in ipython console, or in an IDE such as Spyder.
- To adjust wind speed (m/s) or direction (radians), open fire_states.py and change the values for V and wind_direction, respectively, in lines 11,12
- To adjust adjust simulation time, edit time_sim in main.py, line 11
