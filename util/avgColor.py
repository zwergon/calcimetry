import argparse
from PIL import Image
import math

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to image")
args = vars(ap.parse_args())
imagePath = args["image"]

def dist(x0,y0,x1,y1):
	a,b = x1-x0,y1-y0
	return math.sqrt(a*a+b*b)

def getAverageRGBCircle(img, x, y, radius):
	r,g,b = 0,0,0
	num = 0
	width, height = img.size
# Iterate through a bounding box in which the circle lies
	for i in range( x-radius, x+radius):
		for j in range(y-radius,y+radius):
			# If the pixel is outside the canvas, skip it
			if (i < 0 or i >= width or j < 0 or j >= height) :continue
			# If the pixel is outside the circle, skip it */
			if (dist(x, y, i, j) > r): continue
			# Get the color from the image, add to a running sum */
			r0,g0,b0=img.getpixel((i,j))
			# print("canal rouge : ",r,"canal vert : ",v,"canal bleu : ",b)
			# summing squares is a trick on purpose !
			r += r0*r0
			g += g0*g0
			b += b0*b0
			num+=1
	# Return the mean of the R, G, and B components
	return (math.sqrt(r)/num, math.sqrt(g)/num, math.sqrt(b)/num)

img = Image.open(imagePath)
img.show()
print(getAverageRGBCircle(img,50,50,5))