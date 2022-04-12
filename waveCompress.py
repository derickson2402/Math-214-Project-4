#!python3

# You will need to pip install PyWavelets (and possibly numpy and matplotlib)
from matplotlib.image import imread
import numpy as np
import matplotlib.pyplot as plt
import os
import pywt

# Read in our file names and generate a matrix from the image
# imageIn = imread(input("Enter the input filename: "))
# decompLevel = int(input("How many levels of decomposition: "))
imageIn = imread("Images/horses.png")
decompLevel = 2
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
plt.rcParams['figure.figsize'] = [16, 16]
plt.rcParams.update({'font.size': 18})
plt.imshow(np.dstack((arrR, arrG, arrB)))
plt.show()

# Render multiple compression levels for comparison
imageGray = np.mean(imageIn, -1)
coeffsGray = pywt.wavedec2(imageGray, wavelet=motherWave, level=4)
arrGray, coeffSlicesGray = pywt.coeffs_to_array(coeffsGray)
coeffSorted = np.sort(np.abs(arrGray.reshape(-1)))

# Loop through all the compression ratios we want and print them out
for percent in [ 0.1, 0.05, 0.01, 0.005 ] :
	threshold = coeffSorted[int(np.floor((1-percent)*len(coeffSorted)))]
	ind = np.abs(arrGray) > threshold
	filtered = arrGray * ind
	coeffFiltered = pywt.array_to_coeffs(filtered, coeffSlicesGray, output_format='wavedec2')

	# Rebuild the original image from the specified number of coefficients
	reconstruction = pywt.waverec2(coeffFiltered, wavelet=motherWave)
	plt.figure()
	plt.imshow(reconstruction, cmap='gray')
	plt.axis('off')
	plt.rcParams['figure.figsize'] = [8, 8]
	plt.rcParams.update({'font.size': 18})
	plt.title('Compression Ratio = 1:' + str(1.0 / percent))
	plt.show()

