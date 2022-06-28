# ClickClick

This repo contains a python script that creates

1. `csv` files within the input calcimetry for each original Excell.
2. A pandas dataframe of all meta data for all Andra images, saved in pickle
 fomat.
3. Export of the pandas dataframe to individual csv files for each drill
location

# To Do

1. Merge the indivdual csv files of the calcimetry with the drill location
file (`Prog2` or `Prog2bis` in `util/`) - partial progress in
`notebooks/get_set_from_df.ipynb`
2. Work out how to launch `Prog3` or `Prog3bis` from util using the server and
not duplicating what has been done already.