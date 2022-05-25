import argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to csv file")
args = vars(ap.parse_args())
fileName = args["file"]

df = pd.read_csv(fileName,sep=';',encoding='cp1252')
print(df)
ni,nj = df.shape
print(df.shape)
