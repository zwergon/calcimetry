# ai.calcimetry

Pour l'estimation de la calcimétrie à partir d'une carotte de forage par Deep
Learning.

## Directories

### `calcimetry`

Library of functions to use the images server, `use_server.py`, and the MongoDB
server, `mongo_api.py`.

### `clickclick`

A set of python scripts to digitse the Andra phots from the images server
and to then import the data onto the MongDB server.

* `excel2csv.py` - script to go through the Excel files of calcimetry
measurments and extract the measurments into `csv`format.

* `image_clicks.py` - script to click on a series of images of the drill
core to extract the left and right limits of the core, and the top, bottom
and arrow line for each core. It pulls the images from the images server.

* `import_calcimetry_mongodb.py` - script to import the calcimetry data to
the measurement database on the MongoDB server. It checks if the drill name
exists on the images database, and if it does not it will import the data in
the `mesu.csv` file within the directory that corresponds to the drill name.
 If the `mesu.csv` file does not exist it will create it assuming
`excel2csv.py` has been run such that the data has been extracted from the
Excel file into a more useable format. This script should be run after
`import_images_mongodb.py`. The location of the files to be imported is hard
 coded into the script (line 23).

* `import_images_mongodb.py` - script to import the image data to the images
 database on the MongoDB server. It checks if the drill name exists on the
MongoDB server, and if it does not it will import the data in the `imgs2.csv`
file within the directory that corresponds to the drill name. This therefore
 has to be run after `image_clicks.py`. The location of the files to be
imported is hard coded into the script (line 21).

#### Drill names still to do:

OHZ7008
OHZ7101
OHZ7102
OMA4003
PAC1001
PAC1002
PAC2003

### `notebooks`

* `QC-measurements.ipynb` - Notebook to check what drill names are on the
MongoDB and check number of datapoints within the database correspond with
those on the local machine.

* `open-image-calcimetry.ipynb` - Notebook to plot an image and the
corresponding calcimetry measurements.

* `single_calcimetry_import.ipynb` - Notebook to import calcimetry data to
the MongoDB when the file format does not work with the clickclick script.

* `single_cimage_import.ipynb` - Notebook to import image data to the MongoDB
when the file format does not work with the clickclick script.

## Utilisation du serveur d'image

On trouve le fichier `database/use_server.py` qui illustre comment lire une image jpg 
d'une image de carotte __brute__ comme fournie par l'andra

Le serveur est installé sur `islin-hdpmas1` et tourne à l'adresse suivante `http://imgserver.10.68.0.250.nip.io`
> Attention, cette adresse doit être adressée directement sans passer par le proxy, sinon la requête échoue avec un code 403

Si dans le répertoire database, vous lancez la commande

```
python use_server.py
``` 

Cela devrait vous lister les 10 premiers fichiers de la liste et vous afficher une image au hasard.

