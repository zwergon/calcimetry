import argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-f1", "--file1", required=True, help="Path to calcimetry csv input file1")
ap.add_argument("-f2", "--file2", required=True, help="Path to csv input file2 to complete")
ap.add_argument("-o", "--output", required=True, help="Path to csv output file")
args = vars(ap.parse_args())
fileName1 = args["file1"]
fileName2 = args["file2"]
output = args["output"]

df1 = pd.read_csv(fileName1,sep=';',encoding='cp1252', index_col=False)
# print(dfi)
# ni,nj = dfi.shape
# print(dfi.shape)

df2 = pd.read_csv(fileName2,sep=';',encoding='cp1252', index_col=False)
# print(dfo)

sery0 = pd.Series(dtype='str')
sery1 = pd.Series(dtype='str')
sery2 = pd.Series(dtype='str')

for i, j in df2.iterrows():
    cote0,cote1 = int(round(float(j["Cote0"]))),int(round(float(j["Cote1"])))
    s0,s1,s2 = "{","{","{"
    for k1, k2 in df1.iterrows():
        c = int(round(float(str(k2["Cote"]).replace(',','.'))*100))
        if cote0<=c and c<=cote1:
            if len(s0)!=1 : 
                s0+= ";"
                s1+= ";"
                s2+= ";"
            s0+= str(c)
            s1+= str(df1.iloc[k1, 1]) #str(k2["% calcimétrie 1 min "]) #
            s2+= str(df1.iloc[k1, 3]) #str(k2["% calcimétrie 15 min"]) # 
    s0+= "}"
    s1+= "}"
    s2+= "}"
    sery0.at[i] = s0
    sery1.at[i] = s1
    sery2.at[i] = s2

df2["CalciCotes"]= sery0
df2["CalciVals1m"]= sery1
df2["CalciVals15m"]= sery2

df2.to_csv(output,sep=';',encoding='cp1252',decimal=',')


