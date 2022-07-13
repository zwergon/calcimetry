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
python image_clicks.py -f ~/data/csvs/REP3/PEP1001/Photos/imgs.csv -o ~/data/csvs/REP3/PEP1001/Photos/imgs2.csv
```


