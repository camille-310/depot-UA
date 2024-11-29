#!/bin/env python

import os
from base_livre import *
from fonctions import *
from PyPDF2 import PdfReader
from langdetect import detect

class PDF(base_livre):

    def __init__(self,ressource): # c'est un fichier local ou une url
        if "https" in ressource:   # si c'est une url
            self.ressource = telecharger_url(ressource,'bibliothèque')     # voir fonction telecharger_url dans fonctions
        else:     # si c'est un fichier local
            self.ressource = ressource
        document = PdfReader(open(self.ressource, 'rb'))
        self.metadata = document.metadata
        self._type = "PDF"
        self._titre = self.metadata.get('/Title', 'Titre inconnu')
        self._auteur = self.metadata.get('/Author', 'Auteur inconnu')
        self._langue = self.metadata.get('/Lang')
        self._sujet = self.metadata.get('/Subject', 'Sujet inconnu')
        self._date = self.metadata.get('/CreationDate', 'Date inconnue')

    def type(self):
        return self._type

    def titre(self):
        return self._titre

    def auteur(self):
        return self._auteur

    def langue(self):
        if self._langue:
            return self._langue
        else:
            with open(self.ressource, 'rb') as doc:
                fichier = PdfReader(doc)
                text = "".join(page.extract_text() for page in fichier.pages) # on extrait le texte de toutes les pages
            if text.strip(): # si le texte n'est pas vide :
                self._langue = detect(text)
            else:
                self._langue = "Langue inconnue"
            return self._langue

    def sujet(self):
        return self._sujet

    def date(self):
        return self._date

if __name__ == "__main__":

    fichier_pdf = PDF('./bibliothèque/about_a_b_c_du_travailleur.pdf')

    print("Type :", fichier_pdf.type())
    print("Titre :", fichier_pdf.titre())
    print("Auteur :", fichier_pdf.auteur())
    print("Langue :", fichier_pdf.langue())
    print("Sujet :", fichier_pdf.sujet())

    print("Date :", fichier_pdf.date())

    url_pdf = PDF('https://math.univ-angers.fr/~jaclin/biblio/livres/aicard_illustre_maurin.pdf')

    print("Type :", url_pdf.type())
    print("Titre :", url_pdf.titre())
    print("Auteur :", url_pdf.auteur())
    print("Langue :", url_pdf.langue())
    print("Sujet :", url_pdf.sujet())
    print("Date :", url_pdf.date())
