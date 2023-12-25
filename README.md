# This project is for scripts written in python 3 with Numpy and Matplotlib installed.

## Rainbow_spectrum.py
Draw a spectrum fill by rainbow colors, and the abscissa of the spectrum is the wavelength data in nanometers. There is a corresponding color fill only in the visible region (380-780nm), but the spectral wavelength range is not limited to the visible region. The interval of wavelength data is arbitrary; but keep in mind that the smaller the interval, the better the drawing.

效果如下：

[color_scatter_plot](C:\\Users\\JHL\\Desktop\\8\\color_scatter_plot2.png)

## color_scatter.py
Draw a colorful scatter plot with the color of the dots being gradient filled with blue-green-red colors based on the abscissa values of your data. Since the data ranges of the two gradient parts are not the same, one color range of the drawing is scaled. This script is used to plot the output.txt file obtained by analyzing weak interactions using Multiwfn <http://sobereva.com/399>.
