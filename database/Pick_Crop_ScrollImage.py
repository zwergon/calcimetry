from tkinter import *
from PIL import Image, ImageTk
import argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
fileName = args["image"]
ImmPt = []

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
		global fileName
		self.im=Image.open(fileName)
		global imm
		imm = self.im
		print(self.im,"  ",type(self.im))
		width,height=self.im.size
		print(width,"  ",height)
		canv.config(scrollregion=(0,0,width,height))
		self.im2=ImageTk.PhotoImage(self.im)
		self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)
		print(self.imgtag)

		for x in range(0, 4000, 20):
			canv.create_line(x,0,x,2000, fill='#FFFFFF')
		for y in range(0, 2000, 20):
			canv.create_line(0,y,4000,y, fill='#FFFFFF')

		canv.bind("<Button 1>",getorigin)
		canv.bind("<Button 3>",press)
		canv.bind("<ButtonRelease-3>",release)

def getorigin(eventorigin):
	global imm
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	print(eventorigin.x,eventorigin.y,"  ",x,y," RGB: ",imm.getpixel((int(x),int(y))))
#mouseclick event

def press(eventorigin):
	global ImmPt
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	ImmPt = [(x, y)]
	print("Press ",x,y)

def release(eventorigin):
	global ImmPt
	canvas = eventorigin.widget
	x = canvas.canvasx(eventorigin.x)
	y = canvas.canvasy(eventorigin.y)
	ImmPt.append((x, y))
	canvas.create_rectangle(ImmPt[0][0],ImmPt[0][1], ImmPt[1][0],ImmPt[1][1], outline='#FF0000')
	print("Release ",x,y)

ScrolledCanvas().mainloop()