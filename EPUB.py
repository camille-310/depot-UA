#!/bin/env python

import os
from base_livre import *
from fonctions import *
from ebooklib import epub

class EPUB(base_livre):

    def __init__(self,ressource):
        if "https" in ressource:    # si c'est une url :
            self.ressource = telecharger_url(ressource,'bibliothèque')
        else:                       # si c'est un fichier :
            self.ressource = ressource
        book = epub.read_epub(self.ressource)
        self._type = "EPUB"
        self._titre = book.get_metadata('DC', 'title')[0][0]
        self._auteur = book.get_metadata('DC', 'creator')[0][0]
        self._langue = book.get_metadata('DC', 'language')[0][0]
        self._sujet = book.get_metadata('DC', 'subject')[0][0]
        self._date = book.get_metadata('DC', 'date')


    def type(self):
        return self._type

    def titre(self):
        if len(self._titre)!=0:
            return self._titre
        else:
            return 'Titre inconnu'

    def auteur(self):
        if len(self._auteur)!=0:
            return self._auteur
        else:
            return 'Auteur inconnu'

    def langue(self):
        if len(self._langue)!=0:
            return self._langue
        else:
            return 'Langue inconnue'

    def sujet(self):
        if len(self._sujet)!=0:
            return self._sujet
        else:
            return 'Sujet inconnu'

    def date(self):
        if len(self._date)!=0:
            return self._date
        else:
            return 'Date inconnue'

if __name__ == "__main__":

    fichier_epub = EPUB('./bibliothèque/adam_paul_-_le_conte_futur.epub')   # on teste avec un fichier local (déjà téléchargé)

    print("Titre:", fichier_epub.titre())
    print("Auteur:", fichier_epub.auteur())
    print("Type:", fichier_epub.type())
    print("Langue:", fichier_epub.langue())
    print("Date:", fichier_epub.date())
    print("Sujet:", fichier_epub.sujet())

    url_epub = EPUB('https://math.univ-angers.fr/~jaclin/biblio/livres/aimard_gustave_-_jim_l_indien.epub')   # on teste avec une url

    print("Titre:", url_epub.titre())
    print("Auteur:", url_epub.auteur())
    print("Type:", url_epub.type())
    print("Langue:", url_epub.langue())
    print("Date:", url_epub.date())
    print("Sujet:", url_epub.sujet())





