# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 12:18:22 2021
@author: James Howard
"""

import os
import pandas as pd

class JascoScanFile():
    '''
    Parses JASCO CD Spectrometer formatted .csv files
    '''
    def __init__(self, file):
        self.file = file
        #Check to see if the file is a JASCO formatted csv
        if self.file[-4:] == ".csv" or ".CSV":
            self.content = pd.read_csv((self.file), header=None, sep='\n')
            self.content = self.content[0].str.split(',', expand=True)
            if self.content[1][2] != "JASCO":
                raise ValueError("The file is not formatted like a JASCO .csv file")
        else:
            raise ValueError("The file is not a .csv file")
  
    def get_filepath(self):
        return os.path.abspath(self.file)
    
    def get_content(self):
        return self.content
    
    def name(self):
        return self.content[1][0]
    
    def aquisition_date(self):
        return self.content[1][4]
    
    def aquisition_time(self):
        return self.content[1][5]
    
    def get_wavelengths(self):
        FIRSTX = float(self.content[1][14]) #These array positions are hard coded, so they may have to be changed
        wl = []
        if float(self.content[0][21]) == FIRSTX:
            for point in range(int(self.content[1][16])):
                wl.append(float(self.content[0][21 + point]))
        return wl
    
    def get_CD(self):
        FIRSTX = float(self.content[1][14]) #These array positions are hard coded, so they may have to be changed 
        cd = {}
        if float(self.content[0][21]) == FIRSTX and self.content[1][11] == "CD [mdeg]":
            for point in range(int(self.content[1][16])):
                cd[float(self.content[0][21 + point])] = float(self.content[1][21 + point])
        else:
            print('There was a problem getting the CD data')
        return cd
    
    def get_abs(self):
        FIRSTX = float(self.content[1][14]) #These array positions are hard coded, so they may have to be changed 
        absorbance = {}
        if float(self.content[0][21]) == FIRSTX and self.content[1][13] == "ABSORBANCE":
            for point in range(int(self.content[1][16])):
                absorbance[float(self.content[0][21 + point])] = float(self.content[3][21 + point])
        else:
            print('There was a problem getting the CD data')
        return absorbance
    
    def get_max_CD(self):
        cd = self.get_CD()
        
        if abs(min(cd.values())) > abs(max(cd.values())):
            maxCD = min(cd.values())
        else:
            maxCD = max(cd.values())
        return (list(cd.values()).index(maxCD), maxCD)