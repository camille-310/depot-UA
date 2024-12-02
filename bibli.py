#!/bin/env python

from simple_bibli import *
from fonctions import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Il est demandé une classe identique à simple_bibli avec alimenter en plus, on peut donc la faire hériter de simple_bibli et y mettre seulement alimenter !

class bibli(simple_bibli):
  
  def alimenter(self,url):
    try:
      # Récupérer le contenu de la page
      response = requests.get(url, verify=False, timeout=10)
      response.raise_for_status()
      contenu_html = response.text
    except requests.exceptions.RequestException as e:
      print(f"Erreur lors de l'accès à {url} : {e}")
      return

    # Analyse le HTML avec BeautifulSoup
    analyse = BeautifulSoup(contenu_html, 'html.parser')
    # Trouve toutes les balises 'a' (liens) dans le HTML
    liens = analyse.find_all('a')
    
    if len(liens) == 0:
      print(f"Aucun lien trouvé sur la page {url}")
      return
    
    for lien_init in liens[:10]: # on s'arrête ici à 10 liens
      href = lien_init.get('href')
      if not href:
        continue  # Ignore les liens sans href
      
      lien = urljoin(url, href)
      try:
        if lien.lower().endswith('.pdf'):
          livre = PDF(lien)
          self.ajouter(livre)
        elif lien.lower().endswith('.epub'):
          livre = EPUB(lien)
          self.ajouter(livre)
      except Exception as e:
        print(f"Erreur lors du traitement du lien")

if __name__ == "__main__":

    h = bibli('bibli_test')
    h.alimenter('https://math.univ-angers.fr/~jaclin/biblio/livres/')

    h.rapport_livres("EPUB", "rapport_bibli_livres.epub")
    h.rapport_auteurs("EPUB", "rapport_bibli_auteurs.epub")

    h.rapport_livres("PDF", "rapport_bibli_livres.pdf")
    h.rapport_auteurs("PDF", "rapport_bibli_auteurs.pdf")
