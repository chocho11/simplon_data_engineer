import requests
import time
import csv
import os

dossier_nfs = "C:\\Users\\ten_d\\exos python\\" # "/srv/nfs_share/"
t_stmp = str(time.time()).replace(".","_")

urlproduits = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
urlmagasins = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
urlventes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"



urls = {
        "produit": {"url": urlproduits},
        "magasin": {"url": urlmagasins},
        "vente": {"url": urlventes}
    }

 
def fail_file(file, resp):
    print("Annulation: la procédure de récupération du fichier " + file + "s a échoué.\n", resp)
    exit()



for u in urls:
     
    fields_insert = ""
    vals_insert = []
    interro_pts = ""
    response = None
    
    try:
        response = requests.get(urls[u]['url'])
    except Exception as err1:
        fail_file(u, response)

    if response.status_code != 200:
        fail_file(u, response)
  
    with open(dossier_nfs + t_stmp + "_" + u + "s.csv", "wb") as fichier_local:
        fichier_local.write(response.content) 
  

    # os.remove(t_stmp + "_" + u + "s.csv")

print('Fini')