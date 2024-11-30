#!/bin/env python

import os
import requests

def telecharger_url(url,dossier):

    chemin_fichier = os.path.join(dossier,os.path.basename(url))
    reponse = requests.get(url, verify=False)
    with open(chemin_fichier, 'wb') as doc:
                doc.write(reponse.content)
    return chemin_fichier

def type_contenu(url):
    try:
        # Envoyer une requête HEAD pour récupérer les en-têtes
        response = requests.head(url)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Récupérer le type du contenu
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Déterminer le type en fonction de Content-Type
            if "application/pdf" in content_type:
                return "PDF"
            elif "application/epub+zip" in content_type:
                return "EPUB"
            elif "text/html" in content_type:
                return "HTML"
            else:
                return f"Autre type"
        else:
            return f"Échec de la requête. Statut code : {response.status_code}"
    except requests.RequestException as e:
        return f"Erreur de connexion : {e}"
