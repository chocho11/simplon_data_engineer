import time
import csv
import sqlite3
import os

datalake = "C:\\Users\\ten_d\\exos python\\" # c'est le dossier NFS servant de datalake aussi
t_stmp = ''

def create_tbl(cur):
    cur.execute("""
        CREATE TABLE  IF NOT EXISTS produit (
            id TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            stock INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE  IF NOT EXISTS magasin (
            id INTEGER PRIMARY KEY,
            ville TEXT NOT NULL,
            nb_salaries INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE  IF NOT EXISTS vente (
            date TEXT NOT NULL,
            id_produit TEXT NOT NULL,
            id_magasin INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            PRIMARY KEY (id_produit, id_magasin, date),
            FOREIGN KEY (id_produit) REFERENCES produit(id),
            FOREIGN KEY (id_magasin) REFERENCES magasin(id)
        );
    """)

    cur.execute("""
        CREATE TABLE  IF NOT EXISTS chiffre_affaire (
            date TEXT NOT NULL,
            chiffre_affaire_total INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE  IF NOT EXISTS chiffre_affaire (
            date TEXT NOT NULL,
            chiffre_affaire_total INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventes_produits (
            date TEXT NOT NULL,
            produit TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            chiffre_affaire INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventes_villes (
            date TEXT NOT NULL,
            ville TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            chiffre_affaire INTEGER NOT NULL
        );
    """)

# Lister uniquement les fichiers avec l'extension .csv
fichiers_csv = [f for f in os.listdir(datalake) if f.endswith('.csv')]

# Trier par date de modification (ordre décroissant)
fichiers_csv_trie = sorted(
    fichiers_csv, 
    key=lambda f: os.path.getmtime(os.path.join(datalake, f)), 
    reverse=True
)

for fichier in fichiers_csv_trie:
    if fichier.endswith('_ventes.csv'):
        t_stmp = fichier.replace('_ventes.csv','')
        break;

if t_stmp =='' :
    print('Annulation, pas de fichiers ventes.csv')
    exit()

connexion = sqlite3.connect('ma_base_de_donnees.db')
curseur = connexion.cursor()
create_tbl(curseur)

urls = {
        "produit": {"db_fields":["id"], "f_fields": ["ID Référence produit"],
                        "match_fields": 
                        {
                            "id": ["ID Référence produit", 'str'],
                            "nom": ["Nom", 'str'],
                            "prix": ["Prix", 'float'],
                            "stock": ["Stock", 'int'] 
                        }
                    },

        "magasin": {"db_fields": ["id"], "f_fields": ["ID Magasin"],
                        "match_fields":
                        {
                            "id": ["ID Magasin", 'str'],
                            "ville": ["Ville", 'str'], 
                            "nb_salaries": ["Nombre de salariés", 'int']  
                        }
                    
                    
                    },
        "vente": {"db_fields": ["date", "id_produit", "id_magasin"] ,"f_fields": ["Date", "ID Référence produit", "ID Magasin"],
                  "match_fields":
                  {
                    "date": ["Date", 'str'] ,
                    "id_produit": ["ID Référence produit", 'str'],
                    "id_magasin": ["ID Magasin", 'int'],
                    "quantite": ["Quantité", 'int']
                  }
                }
    }

for u in urls:
    fields_insert = ""
    vals_insert = []
    interro_pts = ""
    
    for mfi in urls[u]['match_fields']:
        if fields_insert != '':
            fields_insert += ','

        if interro_pts != '':
            interro_pts += ','

        fields_insert += mfi
        interro_pts += '?'

    with open(t_stmp + "_" + u + "s.csv", 'r', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier)  # Crée un objet lecteur CSV
        count = 0
        corresp = dict()
        for ligne in lecteur_csv:
            count_mf = 0
            for chmp in ligne:
                for m in urls[u]['match_fields']:
                    if urls[u]['match_fields'][m][0] == chmp:
                        urls[u]['match_fields'][m].append(count_mf)
                        break
                count_mf += 1

        fichier.seek(0)
    
        for ligne in lecteur_csv:
            count2 = 0
            if count == 0:
                 
                for chmp in ligne:
                    count3 = 0 
                    for chmpf in urls[u]['f_fields']:
                        if chmp == chmpf:
                            corresp[chmp] = [urls[u]['db_fields'][count3], count2]
                            break
                        count3 += 1
                    count2 += 1                
                count +=1
                continue

            requete = ""
             
            for s in corresp:
                if requete != "":
                    requete += " AND "    
                requete += "CAST(" + corresp[s][0] + ' AS TEXT) = "' + ligne[corresp[s][1]]  + '"' 

            requete = "SELECT * FROM " + u + " where " + requete
            curseur.execute(requete)
            resultats = curseur.fetchone()
            
            if resultats is None:
                requete = "" 
                get_vals = []
                 
                for mfi in urls[u]['match_fields']:
                    cast_val = ligne[urls[u]['match_fields'][mfi][2]] 
                    match urls[u]['match_fields'][mfi][1]:
                        case 'float':
                            cast_val = float(cast_val)
                        case 'int':
                            cast_val = int(cast_val)
                        case _:
                            cast_val = str(cast_val)
                    
                    get_vals.append(cast_val)   
                vals_insert.append( tuple(get_vals))
 

     
    
    if len(vals_insert) > 0:

        
        curseur.executemany("INSERT INTO " + u + " (" + fields_insert + ") VALUES (" +  interro_pts + ');', vals_insert)
        connexion.commit()
        time.sleep(5)

curseur.execute("""
    INSERT INTO chiffre_affaire (date, chiffre_affaire_total)
    SELECT DATETIME('now') as date, SUM(quantite * prix)  AS chiffre_affaire_total
    FROM vente
    JOIN produit ON vente.id_produit = produit.id;            
""")

curseur.execute("""
    INSERT INTO ventes_produits (date, produit, quantite, chiffre_affaire)
    SELECT DATETIME('now') as date,
        p.nom AS produit,
        SUM(v.quantite) AS quantite_totale,
        SUM(v.quantite * p.prix) AS chiffre_affaires
    FROM vente v
    JOIN produit p ON v.id_produit = p.id
    GROUP BY p.nom;
""")

curseur.execute("""
    INSERT INTO ventes_villes (date, ville, quantite, chiffre_affaire)
    SELECT 
        DATETIME('now') AS date,
        magasin.ville,
        SUM(vente.quantite) AS total_quantite,
        SUM(vente.quantite * produit.prix) AS chiffre_affaires
    FROM vente
    JOIN magasin ON vente.id_magasin = magasin.id
    JOIN produit ON vente.id_produit = produit.id
    GROUP BY magasin.ville
    ORDER BY total_quantite DESC;

""")
connexion.commit()
   
print('Fini')