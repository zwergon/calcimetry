import argparse
import pandas as pd
from PIL import Image, ImageTk

ap = argparse.ArgumentParser()
ap.add_argument("-f1", "--file1", required=True, help="Path to directory")
ap.add_argument("-f2", "--file2", required=True, help="Path to csv input file2 to complete")
ap.add_argument("-o", "--output", required=True, help="name of output file")
args = vars(ap.parse_args())
fileName1 = args["file1"]
fileName2 = args["file2"]
output = args["output"]

df2 = pd.read_csv(fileName2,sep=';',encoding='cp1252')

sery0 = pd.Series(dtype='str')

def px(cote:float,cote0:float,cote1:float,px0:float,px1:float):
	return px0+(px1-px0)*(cote-cote0)/(cote1-cote0)

for i, j in df2.iterrows():
	path = j["Path"]
	img=Image.open(path)
	cote0,cote1 = int(round(float(j["Cote0"]))),int(round(float(j["Cote1"])))
	px0,px1 = int(round(float(j["px0"]))),int(round(float(j["px1"])))
	k_py0,k_py2 = int(round(float(j["k_py0"]))),int(round(float(j["k_py2"])))

	print("img.size : ",img.size)

	s = "{"
	w = j["CalciCotes"]
	for c in w[1:-1].split(';'):
		cote = float(c)
		p = int(round(px(cote,cote0,cote1,px0,px1)))
		#left, upper, right, lower
		box = (p-10, k_py0+10, p+10, k_py2-10)
		print("box : ",box)
		area = img.crop(box)
		nm = 'cropped_'+str(cote)+'.jpg'
		area.save(nm,'jpeg')
		if len(s)!=1 : s+= ";"
		s+= nm
	s+= "}"
	sery0.at[i] = s

df2["Crops"]= sery0
df2.to_csv(output,sep=';',encoding='cp1252',decimal=',')

