import math
import os
import matplotlib.pyplot as plt
from JASCOScanFile import JascoScanFile

def FindCSVs():
    csvs = []
    for file in os.listdir('.'):
        if file[-4:] == ".csv" or file[-5:] == ".CSV":
            csvs.append(file)
    return csvs

def PlotCD(JascoScanFile, plotmax=False, ylimits=None, title=True):
    #Define the scanfile we're working with, get the x and y lists for plotting
    f = JascoScanFile
    cd = f.get_CD()
    x, y = list(cd.keys()), list(cd.values())
    
    #Max CD for scaling Y axis and plotmax
    maxcd = f.get_max_CD()
    if ylimits == None:
        ylim, ylim2 = -abs(maxcd[1]*1.1), abs(maxcd[1]*1.1)
    elif type(ylimits) == tuple:
        ylim, ylim2 = ylimits[0], ylimits[1]
        
    #Wavelengths for scaling X axis
    xlim, xlim2 = min(x), max(x)
    
    #Create figure fig and add an axis, ax
    fig_CD, ax_CD = plt.subplots(1)
    plt.axhline(y=0, color = '#D1D1D1')
    ax_CD.plot(x,y, color='purple')
    ax_CD.set_ylim(ylim, ylim2)
    ax_CD.set_xlim(xlim, xlim2)
    
    #Plotmax=True
    if plotmax == True:
        plt.plot(maxcd[0],maxcd[1], marker='.', color='red')
        plt.text(maxcd[0] + (maxcd[0] * 0.025), maxcd[1] + (maxcd[1] * 0.025), "{} nm, {} mDeg".format(
            str(maxcd[0]), #Wavelength
            str(math.ceil(maxcd[1]*100)/100)), #CD rounded up at the second decimal point
            horizontalalignment='left')

    plt.ylabel("CD (mDeg)")
    plt.xlabel("Wavelength (nm)")
    
    #Title of the figure
    if title == True:               #By default the name of the scanfile
        plt.title(f.name())
    elif isinstance(title, str):    #If it's a string, use that string as title
        plt.title(title)
    plt.show()
    
def PlotAbsorbance(JascoScanFile):
    f = JascoScanFile
    absorbance = f.get_abs()
    x, y = list(absorbance.keys()), list(absorbance.values())
    
    #Wavelengths for scaling X axis
    xlim, xlim2 = min(x), max(x)
    
    fig_ABS, ax_ABS = plt.subplots(1) #Create figure fig and add an axis, ax
    ax_ABS.plot(x,y, color='blue')
    ax_ABS.set_xlim(xlim, xlim2)
    ax_ABS.plot(x,y)
    
    plt.ylabel("Absorbance (au)")
    plt.xlabel("Wavelength (nm)")
    plt.title(f.name())
    plt.show()

csvs = FindCSVs()

for csv in csvs:
    f = JascoScanFile(csv)
    PlotCD(f, plotmax=True, title=True, ylimits=(-50, 50))
    PlotAbsorbance(f)