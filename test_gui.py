# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 18:26:39 2021

@author: James
"""

import tkinter as tk
from tkinter import *
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
        if self.entry.get() == '':
            self.CDPlot = PlotCD(JascoScanFile('S-TMA.csv'), returnfigure=True)
        else:
            self.CDPlot = PlotCD(JascoScanFile('S-TMA.csv'), returnfigure=True, color=str(self.entry.get()))
        print("4")
        self.CDPlot = self.CDPlot.get_tk_widget()
        self.CDPlot.pack()

    def create_entry(self):
        self.entry = tk.Entry()
        self.entry.focus()
        self.entry.pack()

    def create_PlotCD_button(self):
        self.plot_button = tk.Button(root, text = "Plot")
        self.plot_button['command'] = self._PlotCD
        self.plot_button.pack()

    def run(self):
        self.create_entry()
        self.create_PlotCD_button()
        self.root.mainloop()

if __name__=='__main__':
    root = tk.Tk()
    app = App(root)
    app.run()


