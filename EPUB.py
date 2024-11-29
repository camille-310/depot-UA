#!/bin/env python

import os
from base_livre import base_livre

class EPUB(base_livre):

    def __init__(self,ressource): # on part du principe que c'est un fichier
        self.ressource = ressource
        book = ebooklib_epub.read_epub(self.ressource)
        self.type = "EPUB"
        self.titre = book.get_metadata('DC', 'title')[0][0]
        self.auteur = book.get_metadata('DC', 'creator')[0][0]
        self.langue = book.get_metadata('DC', 'language')[0][0]
        self.sujet = book.get_metadata('DC', 'subject')[0][0]
        self.date = book.get_metadata('DC', 'date')[0][0]


    def type(self):
        return self.type

    def titre(self):
        if len(self.titre)!=0:
            return self.titre
        else:
            return 'Titre inconnu'

    def auteur(self):
        if len(self.auteur)!=0:
            return self.auteur
        else:
            return 'Auteur inconnu'

    def langue(self):
        if len(self.langue)!=0:
            return self.langue
        else:
            return 'Langue inconnue'

    def sujet(self):
        if len(self.langue)!=0:
            return self.sujet
        else:
            return 'Sujet inconnu'

    def date(self):
        if len(self.date)!=0:
            return self.date
        else:
            return 'Date inconnue'






