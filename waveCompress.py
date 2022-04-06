#!python3

# You will need to pip install PyWavelets (and possibly numpy and matplotlib)
from matplotlib.image import imread
import numpy as np
import matplotlib.pyplot as plt
import os
import pywt

# Set up our pretty output
plt.rcParams['figure.figsize'] = [16, 16]
plt.rcParams.update({'font.size': 18})

# Read in our file names and generate a matrix from the image
imageIn = imread(input("Enter the input filename: "))
fileNameOut = input("Save to filename: ")
decompLevel = int(input("How many levels of decomposition: "))
image = np.mean(imageIn, -1)

# Perform 2 levels of wavelet decomposition
motherWave = 'db1'
coeffs = pywt.wavedec2(image, wavelet=motherWave, level=decompLevel)

# Normalize the coefficient arrays on each decomp layer
coeffs[0] /= np.abs(coeffs[0]).max()
for layer in range(decompLevel) :
	coeffs[layer + 1] = [d/np.abs(d).max() for d in coeffs[layer + 1]]

arr, coeffSlices = pywt.coeffs_to_array(coeffs)

# Render our grid image, with base waves big on bottom and higher layers
# smaller on top
plt.imshow(arr,cmap='gray_r',vmin=-0.25,vmax=0.75)
# figure = plt.figure(figsize=(18, 16))
plt.show()

# Render multiple compression levels for comparison
# TODO
