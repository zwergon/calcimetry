import io
import os
import random
import requests

def init():
    """
    Set up variables for the server
    """
    # No proxy please
    os.environ['no_proxy']='10.68.0.250.nip.io'

    global __SERVER_URL__
    global __ROOT_PATH__
    # L'adresse du serveur d'image JPEG
    __SERVER_URL__ = 'http://imgserver.10.68.0.250.nip.io'
    # Le répertoire parent sur ce serveur ou chercher des images.
    __ROOT_PATH__ ='/data/andra'
    #print(f"server : {__SERVER_URL__}{__ROOT_PATH__}")
    return __ROOT_PATH__

def get_list(img_path):
    """
    Récupère la liste des noms des images jpeg à partir d'un répertoire racine.
    :param img_path: le chemin racine à partir duquel faire la recherche des images jpeg
    :return: la liste des images jpeg collectée récursivement
    """
    url = __SERVER_URL__ + "/list"
    header = {
        'img_path': img_path
    }
    response = requests.get(url, headers=header)
    code = response.status_code
    print("Status Code", code)
    if code != 200:
        raise Exception(f"no jpg found at {url} ({img_path})")

    files = response.json()
    return files


def get_file(filename, quiet=True):
    """
    Retour une Image (PIL) lue à partir d'un fichier jpeg de la liste
    :param filename: le chemin complet vers le fichier jpeg comme retournée par get_list
    :return: une image (PIL)
    """
    from PIL import Image  
    url = __SERVER_URL__ + "/file"
    header = {
        'filename': filename,
        'Content-type': 'image/jpeg'
    }
    response = requests.get(url, headers=header)
    code = response.status_code
    if quiet == False:
        print("Status Code", code)
    if code == 200:
        return Image.open(io.BytesIO(response.content))


if __name__ == '__main__':
    init()
    files = get_list(__ROOT_PATH__)
    print("nombre de fichiers disponibles", len(files))
    for i in range(10):
        print(files[i])

    idx = int(random.random()*len(files))

    img = get_file(files[idx])
    print(f"image {files[idx]}({idx}) de taille {img.size}")
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.show()
