#!python3
'''#############################################################################

Date
	19 April 2022

Written By
	Dan Erickson (danerick)
	Josh Richman (richmajo)

Course
	Math 214 Linear Algebra

Description
	Image processing script for Capstone Project. Performs 2D wavelet
	transformation on an image, and saves both a composite image showing the
	wavelet layers and a side-by-side comparison image showing the image
	compressed to multiple levels.

	This code is modified from:
	https://github.com/dynamicslab/databook_python

	This code can be accessed at:
	https://github.com/derickson2402/Math-214-Project-4.git

#############################################################################'''

# You will need to pip install PyWavelets (and possibly numpy and matplotlib)
from matplotlib.image import imread
import numpy as np
import matplotlib.pyplot as plt
import os
import pywt

# Read in our file names and generate a matrix from the image
imageIn = imread(input("Enter the input filename: "))
imageOutCompositeName = input("Enter the save filename for composite: ")
imageOutSideName = input("Enter the save filename for side-by-side: ")
decompLevel = int(input("How many levels of decomposition: "))
imageR = imageIn[:, :, 0]
imageG = imageIn[:, :, 1]
imageB = imageIn[:, :, 2]

# Perform 2 levels of wavelet decomposition
motherWave = 'db1'
coeffsR = pywt.wavedec2(imageR, wavelet=motherWave, level=decompLevel)
coeffsG = pywt.wavedec2(imageG, wavelet=motherWave, level=decompLevel)
coeffsB = pywt.wavedec2(imageB, wavelet=motherWave, level=decompLevel)

# Normalize the coefficient arrays on each decomp layer
for coeffs in [ coeffsR, coeffsG, coeffsB ] :
	coeffs[0] /= np.abs(coeffs[0]).max()
	for layer in range(decompLevel) :
		coeffs[layer + 1] = [d/np.abs(d).max() for d in coeffs[layer + 1]]

arrR, coeffSlicesR = pywt.coeffs_to_array(coeffsR)
arrG, coeffSlicesG = pywt.coeffs_to_array(coeffsG)
arrB, coeffSlicesB = pywt.coeffs_to_array(coeffsB)

# Render our grid image, with base waves big on bottom and higher layers
# smaller on top
# plt.imshow(arrGray,cmap='gray_r',vmin=-0.25,vmax=0.75)
# Set up our pretty output
fig = plt.figure(figsize=(8.5, 11))
plt.axis('off')
plt.title("Wavelets Composing Original Image")
plt.rcParams['figure.figsize'] = [16, 16]
plt.imshow(np.dstack((arrR, arrG, arrB)))
fig.savefig(imageOutCompositeName)

# Render multiple compression levels for comparison
imageGray = np.mean(imageIn, -1)
coeffsGray = pywt.wavedec2(imageGray, wavelet=motherWave, level=4)
arrGray, coeffSlicesGray = pywt.coeffs_to_array(coeffsGray)
coeffSorted = np.sort(np.abs(arrGray.reshape(-1)))

# Make our output nice and pretty
fig = plt.figure(figsize=(8.5, 11))
fig.add_subplot(3, 2, 1)
plt.axis('off')
plt.title("Original")
plt.imshow(imageGray, cmap='gray_r', vmin=-0.25, vmax=0.75)

# Loop through all the compression ratios we want and print them out
kept = [ 0.1, 0.01, 0.005, 0.0025, 0.0015 ]
for plot in range(5) :
	fig.add_subplot(3, 2, plot+2)
	threshold = coeffSorted[int(np.floor((1-kept[plot])*len(coeffSorted)))]
	ind = np.abs(arrGray) > threshold
	filtered = arrGray * ind
	coeffFiltered = pywt.array_to_coeffs(filtered, coeffSlicesGray, output_format='wavedec2')

	# Rebuild the original image from the specified number of coefficients
	reconstruction = pywt.waverec2(coeffFiltered, wavelet=motherWave)
	# plt.figure()
	plt.axis('off')
	# plt.rcParams['figure.figsize'] = [8, 8]
	# plt.rcParams.update({'font.size': 18})
	plt.title('Coefficients kept: ' + str(100*kept[plot]) + '%')
	plt.imshow(reconstruction, cmap='gray')
fig.tight_layout()
fig.savefig(imageOutSideName)
