#!/usr/bin/env python

import os
from reportlab.pdfgen import canvas
from ebooklib import epub

class base_bibli:
    def __init__(self, path):
        """ path désigne le répertoire contenant les livres de cette bibliothèque """
        if not os.path.exists(path):
            raise ValueError("Le répertoire spécifié n'existe pas.")
        self.path = path
        self.livres = []

    def ajouter(self, livre):
        """Ajoute un livre à la bibliothèque"""
        if not isinstance(livre, base_livre):
            raise ValueError("L'objet ajouté doit être une instance de base_livre ou de ses sous-classes.")
        self.livres.append(livre)

    def rapport_livres(self, format, fichier):
        """
        Génère un état des livres de la bibliothèque.
        Il contient la liste des livres,
        et pour chacun d'eux
        son titre, son auteur, son type (PDF ou EPUB), et le nom du fichier correspondant.

        format: format du rapport (PDF ou EPUB)
        fichier: nom du fichier généré
        """
        if format not in ["PDF", "EPUB"]:
            raise ValueError("Le format doit être 'PDF' ou 'EPUB'.")
        
        contenu = "Liste des livres dans la bibliothèque :\n\n"
        for livre in self.livres:
            contenu += f"Titre : {livre.titre()}\n"
            contenu += f"Auteur : {livre.auteur()}\n"
            contenu += f"Type : {livre.type()}\n"
            contenu += f"Fichier : {livre.ressource}\n\n"

        if format == "PDF":
            self._generer_pdf(fichier, contenu, type_rapport='bibliothèque')
        elif format == "EPUB":
            self._generer_epub(fichier, contenu, type_rapport='bibliothèque')

    def rapport_auteurs(self, format, fichier):
        """
        Génère un état des auteurs des livres de la bibliothèque.
        Il contient pour chaque auteur
        le titre de ses livres en bibliothèque et le nom du fichier correspondant au livre.

        format: format du rapport (PDF ou EPUB)
        fichier: nom du fichier généré
        """
        if format not in ["PDF", "EPUB"]:
            raise ValueError("Le format doit être 'PDF' ou 'EPUB'.")

        auteurs = {}
        for livre in self.livres:
            auteur = livre.auteur()
            if auteur not in auteurs:
                auteurs[auteur] = []
            auteurs[auteur].append((livre.titre(), livre.type(), livre.ressource))

        contenu = "Liste des auteurs et leurs oeuvres :\n\n"
        for auteur, livres in auteurs.items():
            contenu += f"Auteur : {auteur}\n"
            for titre, type_livre, ressource in livres:
                contenu += f"  - Titre : {titre}, Type : {type_livre}, Fichier : {ressource}\n"
            contenu += "\n"

        if format == "PDF":
            self._generer_pdf(fichier, rapport, type_rapport='auteur')
        elif format == "EPUB":
            self._generer_epub(fichier, rapport, type_rapport='auteur')

    def _generer_pdf(self, fichier, contenu):
        """Génère un fichier PDF."""
        # Taille de la page (Letter/A4)
        width, height = 612, 792 

        # Créer un canvas pour générer le PDF
        pdf = canvas.Canvas(fichier, pagesize=(width, height))

        # Déterminer le titre en fonction du type de rapport
        if type_rapport == 'bibliothèque':
            titre = 'Rapport des livres de la bibliothèque'
        elif type_rapport == 'auteur':
            titre = 'Rapport sur les auteurs et leurs oeuvres'
        else:
            titre = 'Rapport'

        # Ajouter le titre au début du PDF
        pdf.setFont("Times-Roman", 16)
        pdf.drawString(50, height - 50, titre)  # Position du titre au haut de la page

        
        # Ajouter le contenu ligne par ligne
        y = height - 100  # Position de départ en haut de la page
        pdf.setFont("Times-Roman", 12)
        for ligne in contenu.split("\n"):  # découpe le contenue en une liste de chacune de ses lignes
            pdf.drawString(50, y, ligne)  # Ajouter la ligne à la position x=50, y=y
            y -= 15  # Descendre de 15 points pour la prochaine ligne
            if y < 50:  # Nouvelle page si on dépasse la limite inférieure
                pdf.showPage()
                y = height - 50

        # Sauvegarder le fichier PDF
        pdf.save()

    def _generer_epub(self, fichier, contenu, type_rapport):
        """Génère un fichier EPUB."""
        # Créer un nouvel objet EPUB
        livre = epub.EpubBook()

        # Ajouter un titre au fichier
        if type_rapport == 'bibliothèque':
            titre = 'Rapport des livres de la bibliothèque'
        elif type_rapport == 'auteur':
            titre = f'Rapport sur les auteurs et leurs oeuvres'
        else:
            titre = 'Rapport'
        livre.set_title(titre)

        # Créer un chapitre avec le contenu
        chapitre = epub.EpubHtml(title='Rapport', file_name='chapitre.xhtml', lang='fr')
        chapitre.content = f"<h1>Rapport</h1><pre>{contenu}</pre>"

        # Ajouter le chapitre au livre
        livre.add_item(chapitre)

        # Générer le fichier EPUB
        epub.write_epub(fichier, livre)


