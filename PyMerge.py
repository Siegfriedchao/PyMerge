### Written By Youchao Wang, yw479
### 2019.12.14
### Modified 2019.12.16

import os
import shutil
import math
import glob
import numpy as np
import cv2 as cv

# Please set the following parameters
PATH = 'test/'
OUTPUT_PATH = 'output/'
PICTURE_NUMBER = 'A01'
PICTURE_CHANNEL = 'd0'
DIRECTION_FLAG = 'clockwise' # anticlockwise or clockwise

# Initializing environment

def initialize():
	# Sanity check
	if not os.listdir(PATH):
		print("Directory is empty, aborting")
		quit()

	# Create output folder
	if os.path.exists('output/'):
		shutil.rmtree('output/')
	if not os.path.exists('output/'):
		os.makedirs('output/')

	# Create sorted subimages folder
	if os.path.exists(PICTURE_NUMBER + PICTURE_CHANNEL + '/'):
		shutil.rmtree(PICTURE_NUMBER + PICTURE_CHANNEL + '/')
	if not os.path.exists(PICTURE_NUMBER + PICTURE_CHANNEL + '/'):
		os.makedirs(PICTURE_NUMBER + PICTURE_CHANNEL + '/')

	# Copy subimages
	for filename in glob.glob(PATH + '*' + PICTURE_NUMBER + '*' + PICTURE_CHANNEL + '.TIFF'):
		shutil.copy(filename, PICTURE_NUMBER + PICTURE_CHANNEL + '/')

def read_image(PATH):
	# Read all the images
	imageList = []

	# Assuming TIFF format
	for filename in glob.glob(PICTURE_NUMBER + PICTURE_CHANNEL + '/*.TIFF'):
		im = cv.imread(filename)
		imageList.append(im)

	return imageList

def process_image_map(totalSize, isClockwise):
	rowCol = int(math.sqrt(totalSize))
	centre = int(rowCol // 2)
	# print(centre)
	X = centre
	Y = centre
	coordinateList = [[None] * rowCol for i in range(rowCol)]

	direction = 'l'
	if isClockwise:
		left, up, right, down = 1, 1, 2, 2
	else:
		left, down, right, up = 1, 1, 2, 2
	tmp = 0
	j = 0

	for i in range(1, totalSize):
		if (X == 0 and Y == 0) or (X == 0 and Y == (rowCol - 1) ) or (X == (rowCol - 1) and Y == (rowCol - 1) ) or (X == (rowCol - 1) and Y == 0 ):
			j = j - 1
			coordinateList[Y][X] = 999 # this is a magic number, better use enum
		else:
			coordinateList[Y][X] = j
		
		j = j + 1
		# print(X, Y)

		# Algorithm to generate mapping
		# l for left, d for down, r for right, u for up
		if direction == 'l':
			X = X - 1
			tmp += 1
			if (tmp == left):
				if isClockwise:
					direction = 'u'
				else:
					direction = 'd'
				left = left + 2
				tmp = 0
		elif direction == 'u':
			Y = Y - 1
			tmp += 1
			if (tmp == up):
				if isClockwise:
					direction = 'r'
				else:
					direction = 'l'
				up = up + 2
				tmp = 0
		elif direction == 'r':
			X = X + 1
			tmp += 1
			if (tmp == right):
				if isClockwise:
					direction = 'd'
				else:
					direction = 'u'
				right = right + 2
				tmp = 0
		elif direction == 'd':
			Y = Y + 1
			tmp += 1
			if (tmp == down):
				if isClockwise:
					direction = 'l'
				else:
					direction = 'r'
				down = down + 2
				tmp = 0

	coordinateList[Y][X] = 999 # make sure the last corner has been accounted

	return coordinateList

def process_image_map_without_corner(totalSize, isClockwise):
	rowCol = int(math.sqrt(totalSize))
	centre = int(rowCol // 2)
	# print(centre)
	X = centre
	Y = centre
	coordinateList = [[None] * rowCol for i in range(rowCol)]

	direction = 'l'
	if isClockwise:
		left, up, right, down = 1, 1, 2, 2
	else:
		left, down, right, up = 1, 1, 2, 2
	tmp = 0
	j = 0

	for i in range(1, totalSize):
		
		coordinateList[Y][X] = i - 1
		# print(X, Y)

		# Algorithm to generate mapping
		# l for left, d for down, r for right, u for up
		if direction == 'l':
			X = X - 1
			tmp += 1
			if (tmp == left):
				if isClockwise:
					direction = 'u'
				else:
					direction = 'd'
				left = left + 2
				tmp = 0
		elif direction == 'u':
			Y = Y - 1
			tmp += 1
			if (tmp == up):
				if isClockwise:
					direction = 'r'
				else:
					direction = 'l'
				up = up + 2
				tmp = 0
		elif direction == 'r':
			X = X + 1
			tmp += 1
			if (tmp == right):
				if isClockwise:
					direction = 'd'
				else:
					direction = 'u'
				right = right + 2
				tmp = 0
		elif direction == 'd':
			Y = Y + 1
			tmp += 1
			if (tmp == down):
				if isClockwise:
					direction = 'l'
				else:
					direction = 'r'
				down = down + 2
				tmp = 0

	coordinateList[Y][X] = totalSize - 1 # make sure the last corner has been accounted

	return coordinateList

def process_image(imageList):
	# Build up a concat map, assuming a sqaure layout
	# This is for subimages without perfect square
	totalSize = len(imageList) + 4
	isClockwise = 0

	coordinateList = process_image_map(totalSize, isClockwise)

	print('Subimages in the order of')
	for i in coordinateList:
		for tmp in i:
			print('%2d ' % tmp, end = '')
		print()

	return coordinateList

def process_image_without_corner(imageList):
	# Build up a concat map, assuming a sqaure layout
	# This is for 4, 9, 16... subimages
	totalSize = len(imageList)
	isClockwise = 0

	coordinateList = process_image_map_without_corner(totalSize, isClockwise)

	print('Subimages in the order of')
	for i in coordinateList:
		for tmp in i:
			print('%2d ' % tmp, end = '')
		print()

	return coordinateList

def process_image_clockwise(imageList):
	# Build up a concat map, assuming a sqaure layout
	# This is for subimages without perfect square
	# Clock-wise
	totalSize = len(imageList) + 4
	isClockwise = 1

	coordinateList = process_image_map(totalSize, isClockwise)

	print('Subimages in the order of')
	for i in coordinateList:
		for tmp in i:
			print('%2d ' % tmp, end = '')
		print()

	return coordinateList

def process_image_without_corner_clockwise(imageList):
	# Build up a concat map, assuming a sqaure layout
	# This is for 4, 9, 16... subimages
	# Clock-wise
	totalSize = len(imageList)
	isClockwise = 1

	coordinateList = process_image_map_without_corner(totalSize, isClockwise)

	print('Subimages in the order of')
	for i in coordinateList:
		for tmp in i:
			print('%2d ' % tmp, end = '')
		print()

	return coordinateList

def main():

	initialize()

	print('Loading images')
	imageList = read_image(PATH)

	# Sanity check
	isRoot = 0
	testSize = len(imageList)
	root = math.sqrt(testSize)
	if (int(root + 0.5) ** 2 == testSize):
		totalSize = testSize
		isRoot = 1
	else:
		totalSize = testSize + 4
	
	rowCol = int(math.sqrt(totalSize))

	# img = imageList[0]
	# height, width = img.shape[:2]
	# print(height, width)
	if (DIRECTION_FLAG == 'anticlockwise'):
		if isRoot:
			coordinateList = process_image_without_corner(imageList)
		else:
			coordinateList = process_image(imageList)
	elif (DIRECTION_FLAG == 'clockwise'):
		if isRoot:
			coordinateList = process_image_without_corner_clockwise(imageList)
		else:
			coordinateList = process_image_clockwise(imageList)

	imageHorizontalList = []
	# Concat image horizontally
	for rowCount in range(0, rowCol):
		
		if (coordinateList[rowCount][0] == 999):
			img = cv.imread('a.TIFF')
		else:
			img = imageList[coordinateList[rowCount][0]]
			# print('test', coordinateList[rowCount][0])
		for i in range(1, rowCol):
			if (coordinateList[rowCount][i] == 999):
				imgNew = cv.imread('a.TIFF')
			else:
				imgNew = imageList[coordinateList[rowCount][i]]
			img = cv.hconcat([img,imgNew])
			# heightTest, widthTest = img.shape[:2]
			# print(heightTest, widthTest)
			# print(i)
		
		imageHorizontalList.append(img)
		# print('debug')

	# Concat long image into a square image, concat vertically
	img = imageHorizontalList[0]
	for rowCount in range(1, len(imageHorizontalList)):
		imgNew = imageHorizontalList[rowCount]
		img = cv.vconcat([img,imgNew])
		# heightTest, widthTest = img.shape[:2]
		# print(heightTest, widthTest)

	print('Generating image')
	cv.imwrite(OUTPUT_PATH + PICTURE_NUMBER + PICTURE_CHANNEL + '.TIFF', img) 

	print('Complete')


main()