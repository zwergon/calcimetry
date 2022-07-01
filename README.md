# ai.calcimetry

Pour l'estimation de la calcimétrie à partir d'une carotte de forage par Deep Learning.


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

