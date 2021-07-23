import pandas as pd
import os
import matplotlib.pyplot as plt
from JASCOScanFile import JascoScanFile

'''
removes half wavelengths (198.5 nm) from spectra and reorganizes it from the JASCO spectrometers
'''


def FindCSVs():
    csvs = []
    for file in os.listdir('.'):
        if file[-4:] == ".csv" or file[-5:] == ".CSV":
            csvs.append(file)
    return csvs

def PlotCD(JascoScanFile):
    f = JascoScanFile
    
    cd = f.get_CD()
    x, y = cd.keys(), cd.values()
    
    fig_CD, ax_CD = plt.subplots(1) #Create figure fig and add an axis, ax
    plt.axhline(y=0, color = 'black')
    ax_CD.plot(x,y)
    
    
    plt.xlabel("CD (mDeg)")
    plt.xlabel("Wavelength (nm)")
    plt.title(f.name())
    plt.show()
    
def PlotAbsorbance(JascoScanFile):
    f = JascoScanFile
    
    absorbance = f.get_abs()
    x, y = absorbance.keys(), absorbance.values()
    
    fig_ABS, ax_ABS = plt.subplots(1) #Create figure fig and add an axis, ax
    ax_ABS.plot(x,y)
    
    plt.ylabel("Absorbance (au)")
    plt.xlabel("Wavelength (nm)")
    plt.title(f.name())
    plt.show()



d = JascoScanFile("JRH_2074-2-S-PheNA.csv")
content = d.get_content()
PlotCD(d)
PlotAbsorbance(d)