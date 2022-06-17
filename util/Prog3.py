import argparse
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk

Image.MAX_IMAGE_PIXELS = 300000000

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to csv input file to complete")
ap.add_argument("-o", "--output", required=True, help="Path to csv output file")
args = vars(ap.parse_args())
fileName = args["file"]
output = args["output"]

df1 = pd.read_csv(fileName,sep=';',encoding='cp1252')

sery0 = pd.Series(dtype='str')
sery1 = pd.Series(dtype='str')
odd = False
sery2 = pd.Series(dtype='str')
sery3 = pd.Series(dtype='str')
sery4 = pd.Series(dtype='str')
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
		global imm
		imm=Image.open(imageName)
		width,height=imm.size
		canv.config(scrollregion=(0,0,width,height))
		self.im2=ImageTk.PhotoImage(imm)
		self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)

		for x in range(0, 4000, 20):
			canv.create_line(x,0,x,2000, fill='#FFFFFF')
		for y in range(0, 2000, 20):
			canv.create_line(0,y,4000,y, fill='#FFFFFF')

		canv.bind("<Button 1>",getorigin)
		canv.bind("<Button 3>",press)

def press(eventorigin):
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	global sery2,sery3,sery4,k1,state
	if state==0: sery2.at[k1] = str(int(round(y)))
	elif state==1: sery3.at[k1] = str(int(round(y)))
	else: sery4.at[k1] = str(int(round(y)))
	state = (state+1)%3

def getorigin(eventorigin):
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	#print(eventorigin.x,eventorigin.y,"  ",x,y," RGB: ",imm.getpixel((int(x),int(y))))
	global sery0,sery1,k1,odd
	if odd: sery1.at[k1] = str(int(round(x)))
	else: sery0.at[k1] = str(int(round(x)))
	odd = not odd

for k1, k2 in df1.iterrows():
	imageName = k2["Path"]
	print(k2["FileName"],"   ",k2["Cote0"],"  ",k2["Cote1"])
	ScrolledCanvas().mainloop()

df1["px0"]= sery0
df1["px1"]= sery1
df1["k_py0"]= sery2
df1["k_py1"]= sery3
df1["k_py2"]= sery4

df1.to_csv(output,sep=';',encoding='cp1252',decimal=',')

