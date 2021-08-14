# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 18:26:39 2021

@author: James
"""

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PlotJascoData import PlotCD, PlotAbsorbance
from JascoScanFile import JascoScanFile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App():
    def __init__(self, root):
        self.root = root
        self.file = None

    def _PlotCD(self):
        try:
            print("Figure destroyed")
        except:
            pass
        if self.file == None:
            print("File not selected")
            return 0

        ####GETTING THE PLOTTING PARAMETERS#####
        ###COLOR###
        if self.color_entry.get() == '': #Blank color_entry yields purple by default
            color = 'purple'
        else:
            color = str(self.color_entry.get())
        ###TITLE###
        if self.title_entry.get() =='': #Blank title entry yields default title in JASCOScanFile
            title=True
        else:
            title=self.title_entry.get()
        ###YLIMITS###
        ###XLIMITS###
        
        
        self.CDPlot = PlotCD(JascoScanFile(self.file.name), 
                             returnfigure=True, 
                             color=str(color), 
                             plotzeroline=self.plot_zero_line.get(), 
                             title=title,
                             normalize=(self.normalized.get(), self.norm_value_entry.get(), self.norm_wl_entry.get()))
        
        self.canvas = FigureCanvasTkAgg(self.CDPlot, master=self.root)
        self.canvas = self.canvas.get_tk_widget()
        self.canvas.grid(row=20, column=4)

    def _PlotABS(self):
        try:
            print("Figure ABS destroyed")
        except:
            pass
        if self.file == None:
            print("File not selected")
            return 0

        ####GETTING THE PLOTTING PARAMETERS#####
        ###COLOR###
        if self.color_entry.get() == '': #Blank color_entry yields purple by default
            color = 'black'
        else:
            color = str(self.color_entry.get())
        ###TITLE###
        if self.title_entry.get() =='': #Blank title entry yields default title in JASCOScanFile
            title=True
        else:
            title=self.title_entry.get()
        ###YLIMITS###
        ###XLIMITS###
        
        
        self.ABSPlot = PlotAbsorbance(JascoScanFile(self.file.name), returnfigure=True, 
                               color=str(color), title=title, 
                               normalize=(self.normalized.get(), self.norm_value_entry.get(), self.norm_wl_entry.get()))
        self.canvas = FigureCanvasTkAgg(self.ABSPlot, master=self.root)
        self.canvas = self.canvas.get_tk_widget()
        self.canvas.grid(row=20, column=5, padx=20)
    
    def _file_selection(self):
        self.file = filedialog.askopenfile(parent=root, title='Choose a file')
        # If a string is returned from the askopen function (ie file was selected, update file label)
        if self.file != None:
            self.file_selected_label.config(text=self.file.name.split("/")[-1])
        else:
            pass

    def _create_PlotCD_button(self):
        self.plot_button = tk.Button(root, text="Plot")
        self.plot_button['command'] = lambda:[self._PlotCD(), self._PlotABS()]
        self.plot_button.grid(row=1, column=1)

    def _create_left_side_labels(self):
        self.file_label = Label(text="File").grid(row=2, column=0)
        self.title_label = Label(text="Title").grid(row=3, column=0)
        self.color_label = Label(text="Color").grid(row=4, column=0)
        self.normalization_wl = Label(text="Normalization Value").grid(row=5, column=0)
        self.normalization_value = Label(text="Normalization Wavelength").grid(row=6, column=0)

    def _create_select_file_button(self):
        self.plot_button = tk.Button(root, text="Select File")
        self.plot_button['command'] = self._file_selection
        self.plot_button.grid(row=2, column=3)

    def _create_select_file_label(self):
        self.filename = "No file selected"
        self.file_selected_label = tk.Label(
            root, text=self.filename, wraplength=120)
        self.file_selected_label.grid(row=2, column=1)

    def _create_title_entry(self):
        self.title_entry = tk.Entry(relief=SUNKEN)
        self.title_entry.focus()
        self.title_entry.grid(row=3, column=1)

    def _create_color_entry(self):
        self.color_entry = tk.Entry(relief=SUNKEN)
        self.color_entry.focus()
        self.color_entry.grid(row=4, column=1)
        
    def _create_normalization_value_entry(self):
        self.norm_value_entry = tk.Entry(relief=SUNKEN)
        self.norm_value_entry.focus()
        self.norm_value_entry.grid(row=5, column=1)

    def _create_normalization_wavelength_entry(self):
        self.norm_wl_entry = tk.Entry(relief=SUNKEN)
        self.norm_wl_entry.focus()
        self.norm_wl_entry.grid(row=6, column=1)

    def _create_plot_zero_line(self):
        self.plot_zero_line = IntVar()
        self.Checkbutton = tk.Checkbutton(
            root, text="Plot 0 line", variable=self.plot_zero_line)
        self.Checkbutton.grid(row=10, column=1)
    
    def _create_normalized_box(self):
        self.normalized = IntVar()
        self.norm_box = tk.Checkbutton(
            root, text="Normalize Spectrum", variable=self.normalized)
        self.norm_box.grid(row=11, column=1)

    def run(self):
        self._create_select_file_button()
        self._create_select_file_label()
        self._create_title_entry()
        self._create_color_entry()
        self._create_PlotCD_button()
        self._create_plot_zero_line()
        self._create_normalized_box()
        self._create_normalization_wavelength_entry()
        self._create_normalization_value_entry()
        self._create_left_side_labels()
        self.root.geometry("1280x720")
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('JASCO Plotter')
    app = App(root)
    app.run()
