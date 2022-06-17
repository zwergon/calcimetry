import os
import argparse

"""
For root directory and subDirectories call "python Prog1.py -f directory -o /directory/resultName"
usage : python recursive.py -f rootName -o resultName
"""

command = "python Prog1.py"
opt = ["-f","-o"]
key = ["file","output"]
hlp = ["Path to root directory","result file name"]

ap = argparse.ArgumentParser()
for i in range(len(opt)):
	ap.add_argument(opt[i], "--"+key[i], required=True, help=hlp[i])
args = vars(ap.parse_args())

os.system(command+" "+opt[0]+" "+args[key[0]]+" "+opt[1]+" "+os.path.join(args[key[0]], args[key[1]]))
for root, dirs, files in os.walk(args[key[0]]):
	for name in dirs:
		if name != "Photos" : continue
		if os.path.exists('tmp.txt'):
			fp = open('tmp.txt', "r")
			read = fp.read()
			fp.close()
			os.remove('tmp.txt')
		dir = os.path.join(root, name)
		print("QQ  ",dir)
		os.system(command+" "+opt[0]+" "+dir+" "+opt[1]+" "+os.path.join(dir, args[key[1]])+" -n "+read)

if os.path.exists('tmp.txt'):
	os.remove('tmp.txt')