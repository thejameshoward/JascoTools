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
import PIL
from PIL import ImageTk, Image, ImageDraw


class App():
    def __init__(self, root):
        self.root = root
        self.file = None

    def _PlotCD(self):
        try:
            self.canvas_CD.destroy()
        except:
            pass
        if self.file == None:
            print("File not selected")
            return 0

        # Color
        if self.color_entry.get() == '': #Blank color_entry yields purple by default
            color = 'purple'
        else:
            color = str(self.color_entry.get())

        # Title
        if self.title_entry.get() =='': #Blank title entry yields default title in JASCOScanFile
            title=True
        else:
            title=self.title_entry.get()


        # Ylimits
        try:
            ylimits = (float(self.ylim_min.get()), float(self.ylim_max.get()))
        except ValueError:
            ylimits=None
            print("Y limits have been set to default")

        ###XLIMITS###

        self.CDPlot = PlotCD(JascoScanFile(self.file.name),
                             returnfigure=True,
                             color=str(color),
                             plotzeroline=self.plot_zero_line.get(),
                             title=title,
                             normalize=(self.normalized.get(), self.norm_value_entry.get(), self.norm_wl_entry.get()),
                             plotmax=self.max_cd_marker.get(),
                             ylimits=ylimits,
                             truncate=(self.truncate_lower.get(), self.truncate_upper.get()))

        self.canvas_CD = FigureCanvasTkAgg(self.CDPlot, master=self.root)
        self.canvas_CD = self.canvas_CD.get_tk_widget()
        self.canvas_CD.grid(row=20, column=4)

    def _PlotABS(self):
        try:
            self.canvas_ABS.destroy()
        except:
            pass
        if self.file == None:
            return 0

        # Color
        if self.color_entry.get() == '': #Blank color_entry yields purple by default
            color = 'purple'
        else:
            color = str(self.color_entry.get())

        # Title
        if self.title_entry.get() =='': #Blank title entry yields default title in JASCOScanFile
            title=True
        else:
            title=self.title_entry.get()
        ###YLIMITS###
        ###XLIMITS###

        self.ABSPlot = PlotAbsorbance(JascoScanFile(self.file.name),
                                      returnfigure=True,
                                      color=str(color),
                                      title=title,
                                      normalize=(self.normalized.get(), self.norm_value_entry.get(), self.norm_wl_entry.get()),
                                      truncate=(self.truncate_lower.get(), self.truncate_upper.get()))

        self.canvas_ABS = FigureCanvasTkAgg(self.ABSPlot, master=self.root)
        self.canvas_ABS = self.canvas_ABS.get_tk_widget()
        self.canvas_ABS.grid(row=20, column=5, padx=20)

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
        self.ylim_min_label = Label(text="Minimum Y limit").grid(row=7, column=0)
        self.ylim_max_label = Label(text="Maximum Y limit").grid(row=8, column=0)
        self.truncate_lower_label = Label(text="Truncation lower limit").grid(row=9, column=0)
        self.truncate_lower_label = Label(text="Truncation upper limit").grid(row=10, column=0)

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

    def _create_ylim_min_entry(self):
        self.ylim_min = tk.Entry(relief=SUNKEN)
        self.ylim_min.focus()
        self.ylim_min.grid(row=7, column=1)

    def _create_ylim_max_entry(self):
        self.ylim_max = tk.Entry(relief=SUNKEN)
        self.ylim_max.focus()
        self.ylim_max.grid(row=8, column=1)

    def _create_truncate_lower_entry(self):
        self.truncate_lower = tk.Entry(relief=SUNKEN)
        self.truncate_lower.focus()
        self.truncate_lower.grid(row=9, column=1)

    def _create_truncate_upper_entry(self):
        self.truncate_upper = tk.Entry(relief=SUNKEN)
        self.truncate_upper.focus()
        self.truncate_upper.grid(row=10, column=1)

    def _create_plot_zero_line(self):
        self.plot_zero_line = IntVar()
        self.Checkbutton = tk.Checkbutton(
            root, text="Plot 0 line", variable=self.plot_zero_line)
        self.Checkbutton.grid(row=11, column=1, sticky = W)

    def _create_normalized_box(self):
        self.normalized = IntVar()
        self.norm_box = tk.Checkbutton(
            root, text="Normalize Spectrum", variable=self.normalized)
        self.norm_box.grid(row=12, column=1, sticky = W)

    def _create_max_cd_marker_box(self):
        self.max_cd_marker = IntVar()
        self.max_cd_marker_box = tk.Checkbutton(
            root, text="Max CD marker", variable=self.max_cd_marker)
        self.max_cd_marker_box.grid(row=13, column=1, sticky = W)

    def _create_save_button(self):
        self.save_button = tk.Button(root, text="Save Plots")
        self.save_button['command'] = self.save_plots
        self.save_button.grid(row=50, column=1)

    def fig2img(self, fig):
        """
##########################TO DO##########################
        Parameters
        ----------
        fig : Matplotlib figure

        Returns
        -------
        None.

        """
        buf = io.Bytes()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def save_plots(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".svg") ##############TODO
        if f is None:
            return
        cd_img = self.fig2img(self.CDPlot)
        cd_img.save(f)


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
        self._create_max_cd_marker_box()
        self._create_ylim_min_entry()
        self._create_ylim_max_entry()
        self._create_truncate_lower_entry()
        self._create_truncate_upper_entry()


        self._create_save_button()
        self._create_left_side_labels()
        self.root.geometry("1280x720")
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('JASCO Plotter')
    app = App(root)
    app.run()
