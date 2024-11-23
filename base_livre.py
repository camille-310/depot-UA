!/usr/bin/env python

import os
import PyPDF2
from ebooklib import epub
from langdetect import detect

class base_livre:
  def __init__(self,ressource):
    """ ressource désigne soit le nom de fichier (local) correspondant au livre, soit une URL pointant vers un livre."""
    if not os.path.exists(ressource):
            raise ValueError("Le fichier spécifié n'existe pas.")
        self.ressource = ressource

  def type(self):
    """ renvoie le type (EPUB, PDF, ou autre) du livre """
    with open(self.ressource, 'rb') as f:
            signature = f.read(4)  # Lire les 4 premiers octets
        if signature == b'%PDF':  # Signature typique des fichiers PDF
            return "PDF"
        elif signature[:2] == b'PK':  # Les fichiers EPUB sont des archives ZIP
            return "EPUB"
        else:
            return "INCONNU"

  def titre(self):
    """ renvoie le titre du livre """
    raise NotImplementedError("à définir dans les sous-classes")

  def auteur(self):
    """ renvoie l'auteur du livre """
    raise NotImplementedError("à définir dans les sous-classes")

  def langue(self):
    """ renvoie la langue du livre """
    raise NotImplementedError("à définir dans les sous-classes")

  def sujet(self):
    """ renvoie le sujet du livre """
    raise NotImplementedError("à définir dans les sous-classes")

  def date(self):
    """ renvoie la date de publication du livre """
    raise NotImplementedError("à définir dans les sous-classes")

class LivrePDF(base_livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.metadata = self._extraire_metadata()

    def _extraire_metadata(self):
        """Extraire les métadonnées d'un fichier PDF."""
        metadata = {}
        with open(self.ressource, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            metadata = reader.metadata or {}
        return metadata

    def titre(self):
        return self.metadata.get('/Title', 'Titre inconnu')

    def auteur(self):
        return self.metadata.get('/Author', 'Auteur inconnu')

    def langue(self):
        lang = self.metadata.get('/Lang')
        if not lang:
            with open(self.ressource, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join(page.extract_text() for page in reader.pages[:5])
                lang = detect(text)
        return lang or "Langue inconnue"

    def sujet(self):
        return self.metadata.get('/Subject', 'Sujet inconnu')

    def date(self):
        return self.metadata.get('/CreationDate', 'Date inconnue')

class LivreEPUB(base_livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.metadata = self._extraire_metadata()

    def _extraire_metadata(self):
        """Extraire les métadonnées d'un fichier EPUB."""
        metadata = {}
        book = epub.read_epub(self.ressource)
        metadata['title'] = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else None
        metadata['creator'] = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else None
        metadata['language'] = book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else None
        metadata['subject'] = book.get_metadata('DC', 'subject')[0][0] if book.get_metadata('DC', 'subject') else None
        metadata['date'] = book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else None
        return metadata

    def titre(self):
        return self.metadata.get('title', 'Titre inconnu')

    def auteur(self):
        return self.metadata.get('creator', 'Auteur inconnu')

    def langue(self):
        return self.metadata.get('language', 'Langue inconnue')

    def sujet(self):
        return self.metadata.get('subject', 'Sujet inconnu')

    def date(self):
        return self.metadata.get('date', 'Date inconnue')

