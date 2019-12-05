import os
import numpy as np
import cv2
from skimage.transform import resize
import operator
import math


#Convert list to string
def convert_list_string(s): 
  
    # initialization of string to "" 
    new = "" 
  
    # traverse in the string  
    for x in s: 
        new += x  
  
    # return string  
    return new 



# AEI GENERATOR
def image_center(img, is_round=True):
    y = img.mean(axis=1)
    x = img.mean(axis=0)
    ybar = np.sum(np.arange(y.shape[0]) * y)/np.sum(y)
    xbar = np.sum(np.arange(x.shape[0]) * x)/np.sum(x)
    if is_round:
        return int(round(xbar)), int(round(ybar))
    return xbar, ybar



# Image extraction function/Resizer
def image_extraction(img, resized):
    # Checking for where silhouette actually exists to extract data
    # Min. and Max range of x axis for silhouette
    x_a = np.where(img.mean(axis=0) != 0)[0].min()
    x_b = np.where(img.mean(axis=0) != 0)[0].max()

    y_a = np.where(img.mean(axis=1) != 0)[0].min()
    y_b = np.where(img.mean(axis=1) != 0)[0].max()

    # Find center of original image
    x_center, _ = image_center(img)

    # Setting new size constraints to ensure silhouette is retained
    x_a = x_center-resized[1]//2
    x_b = x_center+resized[1]//2

    # Modifying image such that silhouette is retained and information not lost
    img = img[y_a:y_b, x_a if x_a > 0 else 0:x_b if x_b <
        img.shape[1] else img.shape[1]]
    # Use scipy zoom function to resize image
    return resize(img, resized)



# Divides image into k areas
def image_divide(img, k):
##    windowsize_r = round(img.shape[0]/k)
    windowsize_r = math.floor(img.shape[0]/k)
    windowsize_c = img.shape[1]
    combined = []

    for r in range(0, img.shape[0]-((windowsize_r)//2), windowsize_r):
        for c in range(0, img.shape[1], img.shape[1]):
            window = img[r:r+windowsize_r if r+windowsize_r < img.shape[0] else img.shape[0], c:c+windowsize_c]
            combined.append(window)

    return combined



# To generate AEI of given image sequences
def aei_generate(location):
    files = os.listdir(location)
    imgs = [cv2.imread(location+f, 0) for f in files]
    images = [image_extraction(i, (128, 64)) for i in imgs]

    v = np.absolute(np.diff(images, axis=0))
    aei = np.mean(v, axis=0)

    return aei


# Function to split lists
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

#Check logical array for any True element
def anyTrueCheck(x):
    a = np.transpose(x)
    for i in range(len(a)):
        if a[i] == True:
            return True
        else:
            continue
    return False


#Calculate accuracy
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
