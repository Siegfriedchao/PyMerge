import math
import glob
from PIL import Image


# Read all the images
image_list = []
for filename in glob.glob('test/*.tiff'): #assuming tiff
    im=Image.open(filename)
    image_list.append(im)

unitWidth, unitHeight = im.size

# debug use
print(unitWidth, unitHeight)

im = image_list[3]
im.show()

# im = Image.open('images/MDPC501_191112140001_A01f00d0.TIFF')
# im.show()