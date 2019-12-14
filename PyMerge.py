import math
import glob
from PIL import Image # cannot handle tiff 16bit uncompressed properly
import numpy as np
import cv2 as cv

# Please set the following at your ease
PATH = 'test/*.TIFF'

def read_image(PATH):
# Read all the images
	imageList = []

	for filename in glob.glob(PATH): #assuming tiff
		im = cv.imread(filename)
		imageList.append(im)

	return imageList

def creat_whiteImage(height, width):
# Create filling image, in white
	blankImage = np.zeros((height,width,3), np.uint16)

	return blankImage

def main():

# debug use
# print(unitWidth, unitHeight)

#img = cv.imread('images/MDPC501_191112140001_A01f00d0.TIFF', -1)

	imageList = read_image(PATH)

	img = imageList[0]
	height, width = img.shape[:2]
	print(height, width)
	#img = cv.hconcat([img,img])
	#img = cv.vconcat([img,img])


# build up a concat map, assuming a sqaure layout
	totalSize = len(imageList) + 4
	rowCol = int(math.sqrt(totalSize))
	test = int(rowCol // 2)
	print(test)
	X = test
	Y = test
	coordinateList = [[None] * rowCol for i in range(rowCol)]

	direction = 'l'
	left, up, right, bottom = 1, 1, 2, 2
	tmp = 0
	j = 0

	for i in range(1, totalSize):
		if (X == 0 and Y == 0) or (X == 0 and Y == (rowCol - 1) ) or (X == (rowCol - 1) and Y == (rowCol - 1) ) or (X == (rowCol - 1) and Y == 0 ):
			j = j - 1
			coordinateList[Y][X] = 999
		else:
			coordinateList[Y][X] = j
		
		j = j + 1
		print(X, Y)
		if direction == 'l':
			X = X - 1
			tmp += 1
			if (tmp == left):
				direction = 'u'
				left = left + 2
				tmp = 0
		elif direction == 'u':
			Y = Y - 1
			tmp += 1
			if (tmp == up):
				direction = 'r'
				up = up + 2
				tmp = 0
		elif direction == 'r':
			X = X + 1
			tmp += 1
			if (tmp == right):
				direction = 'b'
				right = right + 2
				tmp = 0
		elif direction == 'b':
			Y = Y + 1
			tmp += 1
			if (tmp == bottom):
				direction = 'l'
				bottom = bottom + 2
				tmp = 0

	coordinateList[Y][X] = 999

	for i in coordinateList:
		for tmp in i:
			print('%2d ' % tmp, end = '')
		print()	

	imageHorizontalList = []
	# concat image horizontally
	for rowCount in range(0, rowCol):
		
		if (coordinateList[rowCount][0] == 999):
			img = cv.imread('a.TIFF')
		else:
			img = imageList[coordinateList[rowCount][0]]
			print('test', coordinateList[rowCount][0])
		for i in range(1, rowCol):
			if (coordinateList[rowCount][i] == 999):
				imgNew = cv.imread('a.TIFF')
			else:
				imgNew = imageList[coordinateList[rowCount][i]]
			img = cv.hconcat([img,imgNew])
			heightTest, widthTest = img.shape[:2]
			print(heightTest, widthTest)
			print(i)
		
		imageHorizontalList.append(img)
		print('debug')

	# concat long image into a square image, concat vertically
	img = imageHorizontalList[0]
	for rowCount in range(1, len(imageHorizontalList)):
		imgNew = imageHorizontalList[rowCount]
		img = cv.vconcat([img,imgNew])
		heightTest, widthTest = img.shape[:2]
		print(heightTest, widthTest)

	# cv.imshow("Image", img)
	# cv.waitKey(0)

	cv.imwrite('output/image.TIFF',img) 
	print(coordinateList[1][1])
	print(coordinateList[1][3])
	print(coordinateList[3][1])
	
main()