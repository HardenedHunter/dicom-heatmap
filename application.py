import pydicom
import numpy as np

from matplotlib import image

from tkinter import filedialog as fd
from tkinter import messagebox

from pydicom.filewriter import dcmwrite


class Application:
    def __init__(self, empty_image, dcm_area, img_area, result_area):
        self.empty_image = empty_image
        self.dcm_area = dcm_area
        self.img_area = img_area
        self.result_area = result_area
        self.dcm = None
        self.img = None

        self.clear_plots()

    def clear_plots(self):
        for canvas, plot in [self.dcm_area.values(), self.img_area.values(), self.result_area.values()]:
            plot.imshow(self.empty_image)
            canvas.draw()

    def pick_dcm_filename(self):
        filepath = fd.askopenfilename(
            title='Open DICOM file', initialdir='/', filetypes=(('DICOM files', '*.dcm'),))

        if filepath:
            self.dcm = pydicom.dcmread(filepath)
            canvas, plot = self.dcm_area.values()
            plot.imshow(self.dcm.pixel_array, cmap='gray')
            canvas.draw()

    def pick_img_filename(self):
        filepath = fd.askopenfilename(
            title='Open heatmap image', initialdir='/', filetypes=(('JPG files', '*.jpg'), ('PNG files', '*.png')))

        if filepath:
            self.img = image.imread(filepath)
            canvas, plot = self.img_area.values()
            plot.imshow(self.img)
            canvas.draw()

    def apply_heatmap(self):
        if self.dcm is None or self.img is None:
            messagebox.showwarning(
                message='Please, select both DICOM and Heatmap files')
            return

        dcm_shape = self.dcm.pixel_array.shape
        img_shape = self.img.shape

        if dcm_shape[0] != img_shape[0] or dcm_shape[1] != img_shape[1]:
            messagebox.showwarning(
                message=f'Files have different resolutions.\nDICOM file is: {dcm_shape[0]}x{dcm_shape[1]}\nHeatmap is: {img_shape[0]}x{img_shape[1]}')
            return

        pixels = np.stack((self.dcm.pixel_array,) * 3, axis=-1)
        pixels = np.ndarray.astype(np.divide(pixels, 16), 'uint8')
        pixels = np.max(np.array([self.img, pixels]), axis=0)

        new_dcm = self.dcm.copy()
        new_dcm.PixelData = pixels
        new_dcm.SeriesNumber += 1

        pydicom.dcmwrite('./result.dcm', new_dcm)

        canvas, plot = self.result_area.values()
        plot.imshow(pixels)
        canvas.draw()
