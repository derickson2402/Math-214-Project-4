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
imageGray = np.mean(imageIn, -1)
imageR = imageIn[:, :, 0]
imageG = imageIn[:, :, 1]
imageB = imageIn[:, :, 2]

# Perform 2 levels of wavelet decomposition
motherWave = 'db1'
coeffsGray = pywt.wavedec2(imageGray, wavelet=motherWave, level=decompLevel)
coeffsR = pywt.wavedec2(imageR, wavelet=motherWave, level=decompLevel)
coeffsG = pywt.wavedec2(imageG, wavelet=motherWave, level=decompLevel)
coeffsB = pywt.wavedec2(imageB, wavelet=motherWave, level=decompLevel)

# Normalize the coefficient arrays on each decomp layer
for coeffs in [ coeffsGray, coeffsR, coeffsG, coeffsB ] :
	coeffs[0] /= np.abs(coeffs[0]).max()
	for layer in range(decompLevel) :
		coeffs[layer + 1] = [d/np.abs(d).max() for d in coeffs[layer + 1]]

arrGray, coeffSlicesGray = pywt.coeffs_to_array(coeffsGray)
arrR, coeffSlicesR = pywt.coeffs_to_array(coeffsR)
arrG, coeffSlicesG = pywt.coeffs_to_array(coeffsG)
arrB, coeffSlicesB = pywt.coeffs_to_array(coeffsB)

# Render our grid image, with base waves big on bottom and higher layers
# smaller on top
# plt.imshow(arrGray,cmap='gray_r',vmin=-0.25,vmax=0.75)
plt.imshow(np.dstack((arrR, arrG, arrB)))

# figure = plt.figure(figsize=(18, 16))
plt.show()

# Render multiple compression levels for comparison
# TODO
