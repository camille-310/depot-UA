#!/bin/env python

import os
import requests
from reportlab.pdfgen import canvas
from ebooklib import epub

def telecharger_url(url,dossier):

    chemin_fichier = os.path.join(dossier,os.path.basename(url))
    reponse = requests.get(url, verify=False)
    with open(chemin_fichier, 'wb') as doc:
                doc.write(reponse.content)
    return chemin_fichier

def _generer_pdf(self, fichier, contenu):
    # Taille de la page (Letter/A4)
    width, height = 612, 792
    # Créer un canvas pour générer le PDF
    pdf = canvas.Canvas(fichier, pagesize=(width, height))
    # Ajouter le contenu ligne par ligne
    y = height - 50  # Position de départ en haut de la page
    for ligne in contenu.split("\n"):  # découpe le contenue en une liste de chacune de ses lignes
        pdf.drawString(50, y, ligne)  # Ajouter la ligne à la position x=50, y=y
        y -= 15  # Descendre de 15 points pour la prochaine ligne
        if y < 50:  # Nouvelle page si on dépasse la limite inférieure
            pdf.showPage()
            y = height - 50
    # Sauvegarder le fichier PDF
    pdf.save()
    
    return "un rapport pdf à été écrit"

def _generer_epub(self, fichier, contenu):
    # Crée un nouvel objet EPUB
    livre = epub.EpubBook()
    # Ajoute un titre au fichier
    livre.set_title(fichier)
    # Crée un chapitre avec le contenu
    chapitre = epub.EpubHtml(title='Rapport', file_name='chapitre.xhtml', lang='fr')
    chapitre.content = f"<h1>Rapport</h1><pre>{contenu}</pre>"
    # Ajoute le chapitre au livre
    livre.add_item(chapitre)
    # Génére le fichier EPUB
    epub.write_epub(fichier, livre)

    return "un rapport epub a été écrit"
