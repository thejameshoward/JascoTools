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


class App():
    def __init__(self, root):
        self.root = root

    def _PlotCD(self):
        try:
            self.CDPlot.destroy()
        except:
            pass
        if self.color_entry.get() == '':
            self.CDPlot = PlotCD(JascoScanFile(
                'S-TMA.csv'), returnfigure=True, plotzeroline=self.plot_zero_line.get())
        else:
            self.CDPlot = PlotCD(JascoScanFile('S-TMA.csv'), returnfigure=True,
                                 color=str(self.color_entry.get()), plotzeroline=self.plot_zero_line.get())
        self.CDPlot = self.CDPlot.get_tk_widget()
        self.CDPlot.grid(row=5, column=4)

    def create_PlotCD_button(self):
        self.plot_button = tk.Button(root, text="Plot")
        self.plot_button['command'] = self._PlotCD
        self.plot_button.grid(row=1, column=1)

    def create_labels(self):
        self.file_label = Label(text="File").grid(row=2, column=0)
        self.color_label = Label(text="Color").grid(row=3, column=0)

    def _file_selection(self):
        self.file = filedialog.askopenfile(parent=root, title='Choose a file')
        if self.file != None:  #If a string is returned from the askopen function (ie file was selected, update file label)
            self.create_select_file_label()
        else:
            pass

    def create_select_file_button(self):
        self.plot_button = tk.Button(root, text="Select File")
        self.plot_button['command'] = self._file_selection
        self.plot_button.grid(row=2, column=3)

    def create_select_file_label(self):
        try:
            filename = self.file.name.split("/")[-1]
        except:
            filename = "No file selected"
        self.file_label = tk.Label(root, text=filename, wraplength=80)
        self.file_label.grid(row=2, column=1)

    def create_color_entry(self):
        self.color_entry = tk.Entry(relief=SUNKEN)
        self.color_entry.focus()
        self.color_entry.grid(row=3, column=1)

    def create_plot_zero_line(self):
        self.plot_zero_line = IntVar()
        self.Checkbutton = tk.Checkbutton(
            root, text="Plot 0 line", variable=self.plot_zero_line)
        self.Checkbutton.grid(row=4, column=1)

    def run(self):
        self.create_select_file_button()
        self.create_select_file_label()
        self.create_color_entry()
        self.create_PlotCD_button()
        self.create_plot_zero_line()
        self.create_labels()
        self.root.geometry("600x400")
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('JASCO Plotter')
    app = App(root)
    app.run()
