import glob,os,sys
from PIL import Image
import argparse
import hashlib

"""
List all jpg of a directory writing a csv output file listing the images their Cotes (depth) and Sizes
usage : python Prog1.py -f directory -o result.csv
"""

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to directory")
ap.add_argument("-o", "--output", required=True, help="Path to csv output file")
ap.add_argument("-n", "--nid", default=0, type=int, help="Image Id starting index")
args = vars(ap.parse_args())
fileName = args["file"]
output = args["output"]
id = args["nid"]

#list = glob.glob("D:\PYTHON\Image/*.jpg")
#list = glob.glob("C:\\Users\diviesr\Desktop\ANDRA\Photos OHZ1302/*.jpg")
fileName += "/*.jpg"
list = glob.glob(fileName)
# print(list)

Image.MAX_IMAGE_PIXELS = 300000000

# def checkInt(str):
	# try: int(str); return True
	# except ValueError: return False

with open(output, 'w') as g:
	g.write("ImageId;Path;FileName;DrillName;Cote0;Cote1;PxSize;PySize\n")
	for l in list:
		s=""
		l1 = os.path.basename(l).split(".")[0]
		l2 = l1.split("_")
		if len(l2)<3: continue
		# id = int(hashlib.md5(l1.encode('utf-8')).hexdigest(), 16)
		# print(l1,"  ",id,"  ",l1.encode('utf-8'),"  ",hashlib.md5(l1.encode('utf-8')).hexdigest()[:16])
		im=Image.open(l)
		width,height=im.size
		s+= str(id)+";"+l+";"+os.path.basename(l)+";"+l2[-3]+";"+l2[-2]+";"+l2[-1]+";"+str(width)+";"+str(height)
		g.write(s+"\n")
		id += 1
	g.close()

#writing current id in tmp file...
with open("tmp.txt", 'w') as g:
	g.write(str(id))
	g.close()

