import os
import pandas as pd
from Normalizer import Normalizer


class JascoScanFile():
    '''
    Parses JASCO CD Spectrometer formatted .csv files
    '''

    def __init__(self, file):
        self.file = file
        # Check to see if the file is a JASCO formatted csv
        if self.file[-4:] == ".csv" or ".CSV":
            self.content = pd.read_csv((self.file), header=None, sep='\n')
            self.content = self.content[0].str.split(',', expand=True)
            if self.content[1][2] != "JASCO":
                raise ValueError(
                    "The file is not formatted like a JASCO .csv file")
        else:
            raise ValueError("The file is not a .csv file")

        self.path = os.path.abspath(self.file)
        self.name = self.content[1][0]
        self.aquisition_date = self.content[1][4]
        self.aquisition_time = self.content[1][5]

    def get_wavelengths(self):
        # These array positions are hard coded, so they may have to be changed
        FIRSTX = float(self.content[1][14])
        wl = []
        if float(self.content[0][21]) == FIRSTX:
            for point in range(int(self.content[1][16])):
                wl.append(float(self.content[0][21 + point]))
        return wl

    def get_CD(self):
        # These array positions are hard coded, so they may have to be changed
        FIRSTX = float(self.content[1][14])
        cd = {}
        if float(self.content[0][21]) == FIRSTX and self.content[1][11] == "CD [mdeg]":
            for point in range(int(self.content[1][16])):
                cd[float(self.content[0][21 + point])
                   ] = float(self.content[1][21 + point])
        else:
            print('There was a problem getting the CD data')
        return cd

    def get_normalized_data(self, normalization_value, wavelength_to_normalize):
        normalized_cd, normalized_absorbance = Normalizer(
            self, normalization_value, wavelength_to_normalize)
        return normalized_cd, normalized_absorbance

    def get_abs(self):
        # These array positions are hard coded, so they may have to be changed
        FIRSTX = float(self.content[1][14])
        absorbance = {}
        if float(self.content[0][21]) == FIRSTX and self.content[1][13] == "ABSORBANCE":
            for point in range(int(self.content[1][16])):
                absorbance[float(self.content[0][21 + point])
                           ] = float(self.content[3][21 + point])
        else:
            print('There was a problem getting the absorbance data')
        return absorbance

    def get_max_CD(self):
        cd = self.get_CD()

        if abs(min(cd.values())) > abs(max(cd.values())):
            maxCD = min(cd.values())
        else:
            maxCD = max(cd.values())
        return (list(cd.keys())[list(cd.values()).index(maxCD)], maxCD)
