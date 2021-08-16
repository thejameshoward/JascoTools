import math
import os
import matplotlib.pyplot as plt
from JascoScanFile import JascoScanFile

def FindCSVs(path):
    csvs = []
    for file in os.listdir(path):
        if file[-4:] == ".csv" or file[-5:] == ".CSV":
            csvs.append(file)
    return csvs

def TruncateSpectrum(spectrum, lowerbound=None, upperbound=None):
    if not bool(lowerbound) and not bool(upperbound):
        print("Truncation requires at least 1 wavelenth cutoff")
        return

    spectrum_copy = spectrum.copy()
    # If only a lowerbound is specified
    if bool(lowerbound) and not bool(upperbound):
        for wavelength, value in spectrum.items():
            if wavelength < float(lowerbound):
                spectrum_copy.pop(wavelength)

    # If only an upperbound is specified
    elif bool(upperbound) and not bool(lowerbound):
        for wavelength, value in spectrum.items():
            if wavelength > float(lowerbound):
                spectrum_copy.pop(wavelength)

    else:
        for wavelength, value in spectrum.items():
            if wavelength < float(lowerbound) or wavelength > float(upperbound):
                spectrum_copy.pop(wavelength)

    return spectrum_copy


def PlotCD(JascoScanFile,
           plotmax=False,
           ylimits=None,
           title=True,
           plotwavelengths=None,
           savefigure=False,
           returnfigure=False,
           color='purple',
           plotzeroline=False,
           normalize=(False, None, None),
           truncate=(None, None)):

    # Define the scanfile we're working with, get the x and y lists for plotting
    f = JascoScanFile

    # If normalizing spectrum
    if normalize[0] == True:
        cd = f.get_normalized_data(normalize[1], normalize[2])[0]
    else:
        cd = f.get_CD()

    # Truncating spectrum
    if bool(truncate[0]) or bool(truncate[1]):
        cd = TruncateSpectrum(cd, truncate[0], truncate[1])

    x, y = list(cd.keys()), list(cd.values())

    #Get the maximum CD
    maxcd = max(y)
    for wl, value in cd.items():
        if value == maxcd:
            maxcd = (wl, value)

    #Y axis scaling
    if ylimits == None:
        ylim, ylim2 = -abs(maxcd[1]*1.1), abs(maxcd[1]*1.1)
    elif type(ylimits) == tuple:
        ylim, ylim2 = ylimits[0], ylimits[1]

    # Wavelengths for scaling X axis
    xlim, xlim2 = min(x), max(x)

    # Create figure fig and add an axis, ax
    fig_CD, ax_CD = plt.subplots(1)

    #Plot a zero line
    if plotzeroline == True:
        plt.axhline(y=0, color='#D1D1D1')

    ax_CD.plot(x, y, color=color)    #Color
    ax_CD.set_ylim(ylim, ylim2)         #ylimits
    ax_CD.set_xlim(xlim, xlim2)         #xlimits

    # Plotmax=True #Cant use JascoScanFile.get_max_CD to support absorbance scaled data
    if plotmax == True:
        plt.plot(maxcd[0], maxcd[1], marker='.', color='red')
        plt.text(maxcd[0] + (maxcd[0] * 0.025), maxcd[1] + (maxcd[1] * 0.025), "{} nm, {} mDeg".format(
            str(maxcd[0]),  # Wavelength
            str(math.ceil(maxcd[1]*100)/100)),  # CD rounded up at the second decimal point
            horizontalalignment='left')

    # Plotwavelengths
    if type(plotwavelengths) == tuple or type(plotwavelengths) == int or type(plotwavelengths) == float:
        d = plotwavelengths
        try:
            for wl in d:
                plt.plot(wl, cd[wl], marker='.', color='red')
                plt.text(wl + (wl * 0.025), cd[wl] + (cd[wl] * 0.025), "{} nm, {} mDeg".format(
                    str(wl),  # Wavelength
                    str(math.ceil(cd[wl]*100)/100)),  # CD rounded up at the second decimal point
                    horizontalalignment='left')
        except(TypeError):
            plt.plot(d, cd[d], marker='.', color='red')
            plt.text(d + (d * 0.025), cd[d] + (cd[d] * 0.025), "{} nm, {} mDeg".format(
                str(d),  # Wavelength
                str(math.ceil(cd[d]*100)/100)),  # CD rounded up at the second decimal point
                horizontalalignment='left')

    plt.ylabel("CD (mDeg)")
    plt.xlabel("Wavelength (nm)")

    # Title of the figure
    if title == True:  #By default the name in the JASCOScanFile
        plt.title(f.name)
    elif isinstance(title, str):  # If it's a string, use that string as title
        plt.title(title)

    #If saving figures, save the CD plots in the plots folder
    if savefigure == True:
        plt.savefig("./plots/{}_CD.svg ".format(f.name), dpi=300, format="svg")
    plt.show()

    #If using in another function, get back a tkinter canvas object
    if returnfigure == True:
        #canvas = FigureCanvasTkAgg(fig_CD)
        return fig_CD #canvas


def PlotAbsorbance(JascoScanFile,
                   plotwavelengths=None,
                   savefigure=False,
                   returnfigure=False,
                   normalize=(False, None, None),
                   color='black',
                   title=True,
                   truncate=(None, None)):

    f = JascoScanFile

    if normalize[0] == True:
        absorbance = f.get_normalized_data(normalize[1], normalize[2])[1]
    else:
        absorbance = f.get_abs()

    if bool(truncate[0]) or bool(truncate[1]):
        absorbance = TruncateSpectrum(absorbance, truncate[0], truncate[1])

    x, y = list(absorbance.keys()), list(absorbance.values())

    # Wavelengths for scaling X axis
    xlim, xlim2 = min(x), max(x)

    fig_ABS, ax_ABS = plt.subplots(1)  # Create figure fig and add an axis, ax
    ax_ABS.plot(x, y, color=color)
    ax_ABS.set_xlim(xlim, xlim2)
    ax_ABS.plot(x, y)

    # Plotwavelengths
    if type(plotwavelengths) == tuple or type(plotwavelengths) == int or type(plotwavelengths) == float:
        d = plotwavelengths
        try:
            for wl in d:
                plt.plot(wl, absorbance[wl], marker='.', color='red')
                plt.text(wl + (wl * 0.045), absorbance[wl] - (absorbance[wl] * 0.025), "{} nm, {} au".format(
                    str(wl),  # Wavelength
                    str(math.ceil(absorbance[wl]*100)/100)),  # CD rounded up at the second decimal point
                    horizontalalignment='left')
        except(TypeError):
            plt.plot(d, absorbance[d], marker='.', color='red')
            plt.text(d + (d * 0.045), absorbance[d] - (absorbance[d] * 0.025), "{} nm, {} au".format(
                str(d),  # Wavelength
                str(math.ceil(absorbance[d]*100)/100)),  # CD rounded up at the second decimal point
                horizontalalignment='left')

    plt.ylabel("Absorbance (au)")
    plt.xlabel("Wavelength (nm)")
    plt.title(f.name)

    # Title of the figure
    if title == True:  #By default the name in the JASCOScanFile
        plt.title(f.name)
    elif isinstance(title, str):  # If it's a string, use that string as title
        plt.title(title)

    #If saving figures, save the CD plots in the plots folder
    if savefigure == True:
        plt.savefig("./plots/{}_ABS.svg".format(f.name), dpi=300, format="svg")
    plt.show()

    #If using in another function, get back a tkinter canvas object
    if returnfigure == True:
        return fig_ABS


if __name__ == "__main__":
    path = "./examples"
    csvs = FindCSVs(path)

    for csv in csvs:
        f = JascoScanFile("./examples/{}".format(csv))
        PlotCD(f, title=False, savefigure=True, plotmax=True, truncate=(210, 230))
        #PlotAbsorbance(f, normalize=(True, 1, 240))
