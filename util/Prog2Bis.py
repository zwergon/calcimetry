import argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-f1", "--file1", required=True, help="Path to calcimetry csv input file1")
ap.add_argument("-f2", "--file2", required=True, help="Path to images csv file2")
ap.add_argument("-o", "--output", required=True, help="Path to measurement csv output file")
ap.add_argument("-n", "--nid", default=0, type=int, help="Measurement Id starting index")
args = vars(ap.parse_args())
fileName1 = args["file1"]
fileName2 = args["file2"]
output = args["output"]
id = args["nid"]

df1 = pd.read_csv(fileName1,sep=';',encoding='cp1252')
df2 = pd.read_csv(fileName2,sep=';',encoding='cp1252')

with open(output, 'w') as g:
	g.write("MeasureId;ImageId;CalciCote;CalciVals1m;CalciVals15m\n")
	for i, j in df2.iterrows():
		imgId,cote0,cote1 = j["ImageId"],int(round(float(j["Cote0"]))),int(round(float(j["Cote1"])))
		for k1, k2 in df1.iterrows():
			c = int(round(float(k2["Cote"].replace(',','.'))*100))
			if cote0<=c and c<=cote1:
				g.write(str(id)+";"+str(imgId)+";"+str(c)+";"+str(df1.iloc[k1, 1])+";"+str(df1.iloc[k1, 3])+"\n")
				id += 1
	g.close()



