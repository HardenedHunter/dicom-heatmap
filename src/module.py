from matplotlib import image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
from application import Application


def build_area(root, title):
    fig = Figure(figsize=(4.5, 4.5), dpi=100)
    fig.set_facecolor('#323232')
    plot = fig.add_subplot(111)
    plot.set_title(title, color='white', size=16)
    plot.axes.get_xaxis().set_visible(False)
    plot.axes.get_yaxis().set_visible(False)
    canvas = FigureCanvasTkAgg(fig, master=root)
    return {'canvas': canvas, 'plot': plot}


root = tk.Tk()
root.title('DICOM Heatmap')
root.resizable(False, False)
root.geometry('780x780')

empty_image = image.imread('no-image.jpeg')
dcm_area = build_area(root, 'DICOM')
img_area = build_area(root, 'Heatmap')
result_area = build_area(root, 'Result')

dcm_area['canvas'].get_tk_widget().place(x=40, y=390)
img_area['canvas'].get_tk_widget().place(x=390, y=40)
result_area['canvas'].get_tk_widget().place(x=390, y=390)


app = Application(empty_image, dcm_area, img_area, result_area)

open_dcm_button = ttk.Button(root, text='Open DICOM File',
                             command=lambda: app.pick_dcm_filename())
open_img_button = ttk.Button(root, text='Open Heatmap',
                             command=lambda: app.pick_img_filename())
apply_heatmap_button = ttk.Button(root, text='Apply Heatmap',
                                  command=lambda: app.apply_heatmap())

block = {'x': 110, 'y': 150}
open_dcm_button.place(x=block['x'], y=block['y'], width=200)
open_img_button.place(x=block['x'], y=block['y'] + 40, width=200)
apply_heatmap_button.place(x=block['x'], y=block['y'] + 80, width=200)

root.mainloop()
