#!/bin/env python

import os
import requests

def telecharger_url(url,dossier):

    chemin_fichier = os.path.join(dossier,os.path.basename(url))
    reponse = requests.get(url, verify=False)
    with open(chemin_fichier, 'wb') as doc:
                doc.write(reponse.content)
    return chemin_fichier
