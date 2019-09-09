# CSE 6730 Project 2
# Travis Burrows

import csv
import numpy as np
import os.path

def readData():
    """
    readData reads data.csv and Veg_Density_Converted.csv and returns data in the form of a dictionary of numpy arrays
    This relies on the two csv files to be in the same directory as the function, else the paths must be modified.
    In addition, the categories of data that are extracted can be changed by modifying the categories variable
    
    How to use:
        
    your_variable_name = readData()
    
    
    How to use dictionary:
    
    Plot contour of slope:
    plt.contourf(datadict["X"],datadict["Y"],datadict["SLP"])
    
    Return 2D array of EVT: 
    datadict['EVT']
    """
    
    print("Reading data...")
    datafile = "data.csv"                               # Specifies path of data csv file
    vegfile = "Veg_Density_Converted.csv"               # Specifies path of Veg_Density_Converted.csv file
    categories = ['X','Y','EVC','EVT','SLP','DEM']      # Specifies data categories desired to be returned
    
    # Reads CSV file into array
    if os.path.isfile(datafile):
        with open(datafile, newline='') as csvfile:
            data = csv.reader(csvfile, dialect='excel',delimiter=',')
            rownum = 0
            array=np.zeros([560157, 14])
            category = []
            for row in data:
                if rownum > 0:
                    for i in range(rowlen):
                        array[rownum-1,i] = int(row[i])
                else:
                    rowlen = np.size(row)
                    for i in range(rowlen):
                        category.append(row[i])
                rownum+=1
    else:
        raise ValueError( "data.csv was not found in the path %s.  Check the datafile variable" % datafile) 
    
    # Converts array into dictionary of arrays
    datadict = {}
    for i in range(rowlen):
        if category[i] in categories:
            datadict[category[i]] = np.reshape(array[:,i],[813,689])
    
    # Reads EVT conversion values specified by Veg_Density_Converted.csv
    if "EVT" in datadict:
        if os.path.isfile(vegfile):
            with open(vegfile, newline='') as csvfile:
                data = csv.reader(csvfile, dialect='excel',delimiter=',')
                rownum = 0
                array=np.zeros([42, 2])
                category = []
                for row in data:
                    if rownum > 0:
                        array[rownum-1,0] = int(row[8])
                        array[rownum-1,1] = int(row[9])
                    rownum+=1
        else:
            raise ValueError( "Veg_Density_Converted.csv was not found in the path %s.  Check the vegfile variable" % vegfile) 
        
        # Converts EVT values to those specified in Veg_Density_Converted.csv
        for i in range(42):
            datadict['EVT'][datadict['EVT']==array[i,0]]=array[i,1]
    
    # Reads EVC conversion values specified by Veg_Density_Converted.csv
    if "EVC" in datadict:
        if os.path.isfile(vegfile):
            with open(vegfile, newline='') as csvfile:
                data = csv.reader(csvfile, dialect='excel',delimiter=',')
                rownum = 0
                array=np.zeros([39, 2])
                category = []
                for row in data:
                    if rownum > 0 and rownum <= 39:
                        array[rownum-1,0] = float(row[0])
                        array[rownum-1,1] = float(row[1])
                    rownum+=1
        else:
            raise ValueError( "Veg_Density_Converted.csv was not found in the path %s.  Check the vegfile variable" % vegfile) 
        
        # Converts EVC values to those specified in Veg_Density_Converted.csv
        for i in range(39):
            datadict['EVC'][datadict['EVC']==array[i,0]]=array[i,1]     
    
    return datadict