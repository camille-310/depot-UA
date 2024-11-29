#!/bin/env python

import os
from base_livre import base_livre
from PyPDF2 import PdfReader
from langdetect import detect

class PDF(base_livre):

    def __init__(self,ressource): # on part du principe que c'est un fichier
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

    Pdf = PDF('./about_a_b_c_du_travailleur.pdf')

    print("Type :", Pdf.type())
    print("Titre :", Pdf.titre())
    print("Auteur :", Pdf.auteur())
    print("Langue :", Pdf.langue())
    print("Sujet :", Pdf.sujet())
    print("Date :", Pdf.date())
