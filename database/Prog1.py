import glob
import os
from PIL import Image

#list = glob.glob("D:\PYTHON\Image/*.jpg")
list = glob.glob("C:\\Users\diviesr\Desktop\ANDRA\Photos OHZ1302/*.jpg")
print(list)

def checkInt(str):
	try: int(str); return True
	except ValueError: return False

outputPath = "result.csv"
with open(outputPath, 'w') as g:
	g.write("Path;FileName;DrillName;Cote0;Cote1;SizePx(Nx);SizePy(Ny)\n")
	for l in list:
		s=""
		ll = os.path.basename(l).split(".")[0]
		l2 = ll.split("_")
		im=Image.open(l)
		width,height=im.size
		s+= l+";"+os.path.basename(l)+";"+l2[-3]+";"+l2[-2]+";"+l2[-1]+";"+str(width)+";"+str(height)
		g.write(s+"\n")
		#print(os.path.splitdrive(l),"  ",os.path.basename(l),"  ",os.path.basename(l).split(".")[0])
		# print(l2)
		# if len(l2) > 2 and checkInt(l2[-2]) and checkInt(l2[-1]): print(int(l2[-2]),"  ",int(l2[-1]))
	g.close()

