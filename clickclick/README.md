# ClickClick

This repo contains a python script that creates

1. `csv` files within the input calcimetry for each original Excell.
2. A pandas dataframe of all meta data for all Andra images, saved in pickle
 fomat.
3. Export of the pandas dataframe to individual csv files for each drill
location
4. `image_clicks.py`

`image_clicks.py` is a modified version of `../util/prog3bis.py` that calls
images off the server assuming I have Renaud's csv files locally. For example:
```console
cd path/to/clickclick
python image_clicks.py -f ~/data/csvs/REP4/PEP1001/Photos/imgs.csv -o ~/data/csvs/REP4/PEP1001/Photos/imgs2.csv
```

5. Import csv data files from the local machine on to the MongDB:
`import_image_mongodb.py`

6. Import the calcimetry measurments from the local machine tot the MongDB:
`import_calcimetry_mongodb.py` tries to import the measurement data to the
measurement database for two cases, the measurement file exists, in which
case it is simply imported, or the measurement file does not exist, in which
 case it is created. This second step assumes that the `excell2csv.py`
 script has already been launched, and for each Excel file there already
 exists a `csv` equivalent.



