

Prog1 :
	List all jpg images of a directory writing a csv output file listing the images their Cotes (depth) and Sizes
	Usage : python Prog1.py -f directory -o result.csv

recursive :
	Calling Prog1 on a each directory and subdirectories writing output in each subdirectories
	Usage : python recursive.py -f directory -o result.csv

Prog2 :
	Complete file with 3 cols from calci.csv (cote, vals1m, vals15m)
	Usage : python Prog2.py -f1 calci.csv -f2 to_complete.csv -o output.csv

Prog2Bis :
	Build measurement file with 5 cols Id & ImageId & from calci.csv (cote, vals1m, vals15m) 
	Usage : python Prog2.py -f1 calci.csv -f2 imgs.csv -o measur.csv -n id

Prog3 :
	Complete file with 5 cols (px0, px1, k_py0, k_py1, k_py2) corresponding to clicks on image display for each line 
	Usage : python Prog3.py -f to_complete.csv -o output.csv

Prog3Bis :
	Complete file with 5 cols (px0, px1, k_py0, k_py1, k_py2) corresponding to clicks on image display for each line 
	Usage : python Prog3Bis.py -f imgs.csv -o imgs2.csv

Prog4 :
	Build Crop file with one column with {cropnames} and output directory with cropImages
	Usage : python Prog4.py -f1 dir -f2 to_complete.csv -o output