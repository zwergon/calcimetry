import argparse
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk

Image.MAX_IMAGE_PIXELS = 300000000

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to image file")
ap.add_argument("-o", "--output", required=True, help="Path to csv output file")
args = vars(ap.parse_args())
fileName = args["file"]
output = args["output"]
x0,y0 = [],[]
state = 0

class ScrolledCanvas(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.master.title("Image Viewer")
		self.pack(expand=YES, fill=BOTH)
		canv = Canvas(self, relief=SUNKEN)
		canv.config(width=1550, height=650)
		canv.config(highlightthickness=0)

		sbarV = Scrollbar(self, orient=VERTICAL)
		sbarH = Scrollbar(self, orient=HORIZONTAL)

		sbarV.config(command=canv.yview)
		sbarH.config(command=canv.xview)

		canv.config(yscrollcommand=sbarV.set)
		canv.config(xscrollcommand=sbarH.set)

		sbarV.pack(side=RIGHT, fill=Y)
		sbarH.pack(side=BOTTOM, fill=X)

		canv.pack(side=LEFT, expand=YES, fill=BOTH)
		global imageName
		imm=Image.open(imageName)
		width,height=imm.size
		canv.config(scrollregion=(0,0,width,height))
		self.im2=ImageTk.PhotoImage(imm)
		self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)

		for x in range(0, 4000, 20):
			canv.create_line(x,0,x,2000, fill='#FFFFFF')
		for y in range(0, 2000, 20):
			canv.create_line(0,y,4000,y, fill='#FFFFFF')

		canv.bind("<Button 1>",click)
		canv.bind("<Button 3>",end)

""" reverse order if x0 is not in creasing order """
def order(x0,y0):
	if x0[0]<=x0[-1]: return
	x0.reverse()
	y0.reverse()

def string(x0,y0):
	if len(y0)==1 : return str(int(round(y0[0])))
	order(x0,y0)
	s="{"
	for i in range(len(x0)):
		if i!=0: s+=";"
		s+="{"+str(int(round(x0[i])))+";"+str(int(round(y0[i])))+"}"
	return s+"}"

def list(string):
	t = string.replace("{","").replace("}","").split(";")
	return [int(i) for i in t[::2]],[int(i) for i in t[1::2]]

def end(eventorigin):
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	global x0,y0,sery2,sery3,k1,state
	n = len(x0)
	if n!=0: canvas.create_line(x0[n-1],y0[n-1],x,y, fill='#FF0000')
	x0.append(x)
	y0.append(y)
	if state==2:
		sery2.at[k1] = string(x0,y0)
		x0,y0 = [],[]
		state=3
	elif state==3:
		sery3.at[k1] = string(x0,y0)
		x0,y0 = [],[]
		state=4
	elif state==4:
		sery4.at[k1] = string(x0,y0)
		x0,y0 = [],[]
		state=5

def click(eventorigin):
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	global sery0,sery1,k1,state
	if state==0:
		sery0.at[k1] = str(int(round(x)))
		state=1
	elif state==1:
		sery1.at[k1] = str(int(round(x)))
		state=2
	else :
		global x0,y0
		n = len(x0)
		if n != 0: canvas.create_line(x0[n-1],y0[n-1],x,y, fill='#FF0000')
		x0.append(x)
		y0.append(y)

df1 = pd.read_csv(fileName,sep=';',encoding='cp1252')

sery0 = pd.Series(dtype='str')
sery1 = pd.Series(dtype='str')
sery2 = pd.Series(dtype='str')
sery3 = pd.Series(dtype='str')
sery4 = pd.Series(dtype='str')

for k1, k2 in df1.iterrows():
	imageName = k2["Path"]
	print(k2["FileName"],"   ",k2["Cote0"],"  ",k2["Cote1"])
	state = 0
	ScrolledCanvas().mainloop()

df1["px0"]= sery0
df1["px1"]= sery1
df1["k_Up"]= sery2
df1["k_Down"]= sery3
df1["k_Arrow"]= sery4

df1.to_csv(output,sep=';',encoding='cp1252',decimal=',', index = False)