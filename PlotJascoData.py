import math
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from JascoScanFile import JascoScanFile


def FindCSVs():
    csvs = []
    for file in os.listdir('.'):
        if file[-4:] == ".csv" or file[-5:] == ".CSV":
            csvs.append(file)
    return csvs


def PlotCD(JascoScanFile, plotmax=False, ylimits=None, title=True, plotwavelengths=None, savefigure=False, returnfigure=False, color='purple'):
    # Define the scanfile we're working with, get the x and y lists for plotting
    f = JascoScanFile
    cd = f.get_CD()
    x, y = list(cd.keys()), list(cd.values())

    # Max CD for scaling Y axis and plotmax
    maxcd = f.get_max_CD()
    if ylimits == None:
        ylim, ylim2 = -abs(maxcd[1]*1.1), abs(maxcd[1]*1.1)
    elif type(ylimits) == tuple:
        ylim, ylim2 = ylimits[0], ylimits[1]

    # Wavelengths for scaling X axis
    xlim, xlim2 = min(x), max(x)

    # Create figure fig and add an axis, ax
    fig_CD, ax_CD = plt.subplots(1)
    plt.axhline(y=0, color='#D1D1D1')   #Solid line at zero
    ax_CD.plot(x, y, color=color)    #Color
    ax_CD.set_ylim(ylim, ylim2)         #ylimits
    ax_CD.set_xlim(xlim, xlim2)         #xlimits

    # Plotmax=True
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
        canvas = FigureCanvasTkAgg(fig_CD)
        return canvas


def PlotAbsorbance(JascoScanFile, plotwavelengths=None, savefigure=False, returnfigure=False):
    f = JascoScanFile
    absorbance = f.get_abs()
    x, y = list(absorbance.keys()), list(absorbance.values())

    # Wavelengths for scaling X axis
    xlim, xlim2 = min(x), max(x)

    fig_ABS, ax_ABS = plt.subplots(1)  # Create figure fig and add an axis, ax
    ax_ABS.plot(x, y, color='blue')
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

    #If saving figures, save the CD plots in the plots folder
    if savefigure == True:
        plt.savefig("./plots/{}_ABS.svg".format(f.name), dpi=300, format="svg")
    plt.show()

    #If using in another function, get back a tkinter canvas object
    if returnfigure == True:
        canvas = FigureCanvasTkAgg(fig_ABS)
        return canvas


if __name__ == "__main__":
    csvs = FindCSVs()

    for csv in csvs:
        f = JascoScanFile(csv)
        PlotCD(f, title=False, savefigure=True, ylimits=(-45,45))
        #PlotAbsorbance(f)
