#!/bin/env python

import os
from base_livre import base_livre
from ebooklib import epub

class EPUB(base_livre):

    def __init__(self,ressource): # on part du principe que c'est un fichier
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

  epub = EPUB('./adam_paul_-_le_conte_futur.epub')

  print("Titre:", epub.titre())
  print("Auteur:", epub.auteur())
  print("Type:", epub.type())
  print("Langue:", epub.langue())
  print("Date:", epub.date())
  print("Sujet:", epub.sujet())





