#!/bin/env python

import os
from EPUB import *
from PDF import *
from reportlab.pdfgen import canvas
from base_bibli import *
from fonctions import _generer_epub, _generer_pdf

class simple_bibli(base_bibli):

    def __init__(self, path):
        if not os.path.exists(path):
            os.makedirs(path)  # Crée le répertoire
            print(f"Répertoire créé : {path}")
        self.repertoire = path
        self.livres = []
        self.formats = ["PDF", "EPUB"]

    def ajouter(self, livre):
        if not isinstance(livre, base_livre):
            raise ValueError("L'objet ajouté doit être une instance de base_livre ou de ses sous-classes.")
        self.livres.append(livre)

    def rapport_livres(self, format, fichier):
        if format not in self.formats:
            raise ValueError("Le format n'est pas accepté.")

        contenu = "Liste des livres dans la bibliothèque :\n\n"
        i = 1
        for livre in self.livres:
            contenu += f"Livre {i} :\n"
            contenu += f"- Titre : {livre.titre()}\n"
            contenu += f"- Auteur : {livre.auteur()}\n"
            contenu += f"- Type : {livre.type()}\n"
            contenu += f"- Fichier : {livre.ressource}\n\n"
            i += 1

        print(contenu)

        if format == "PDF":
            _generer_pdf(self, fichier, contenu)
        elif format == "EPUB":
            _generer_epub(self, fichier, contenu)

    def rapport_auteurs(self, format, fichier):
        if format not in self.formats:
            raise ValueError("Le format n'est pas accepté.")

        auteurs = {}
        for livre in self.livres:
            auteur = livre.auteur()
            if auteur not in auteurs:
                auteurs[auteur] = []
            auteurs[auteur].append((livre.titre(), livre.type(), livre.ressource))

        contenu = "Liste des auteurs et leurs oeuvres :\n\n"
        i = 1
        for auteur, livres in auteurs.items():
            contenu += f"Auteur {i}: {auteur}\n"
            k = 1
            for titre, type_livre, ressource in livres:
                contenu += f"Livre {k} :\n"
                contenu += f"- Titre : {titre}\n"
                contenu += f"- Fichier : {ressource}\n"
                contenu += f"- Type : {type_livre}\n"
                k += 1
            i += 1
            contenu += "\n"

        print(contenu)

        if format == "PDF":
            _generer_pdf(self, fichier, contenu)
        elif format == "EPUB":
            _generer_epub(self, fichier, contenu)


if __name__ == "__main__":

    répertoire = simple_bibli('bibliothèque')
    epub1 = EPUB('./bibliothèque/adam_paul_-_le_conte_futur.epub')
    epub2 = EPUB('https://math.univ-angers.fr/~jaclin/biblio/livres/blasco-ibanez_vicente_-_les_quatre_cavaliers_de_l_apocalypse.epub')
    epub3 = EPUB('https://math.univ-angers.fr/~jaclin/biblio/livres/adam_paul_-_la_glebe.epub') # même auteur que epub1
    pdf1 = PDF('./bibliothèque/about_nez_notaire.pdf')
    pdf2 = PDF('https://math.univ-angers.fr/~jaclin/biblio/livres/bernay-pujol_secret_sunbeam_valley.pdf')

    répertoire.ajouter(epub1)
    répertoire.ajouter(epub2)
    répertoire.ajouter(epub3)
    répertoire.ajouter(pdf1)
    répertoire.ajouter(pdf2)

    répertoire.rapport_livres("EPUB", "rapport_livres.epub")
    répertoire.rapport_auteurs("EPUB", "rapport_auteurs.epub")
    répertoire.rapport_livres("PDF", "rapport_livre.pdf")
    répertoire.rapport_auteurs("PDF", "rapport_auteurs.pdf")
