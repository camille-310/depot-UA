#!/bin/env python

from bibli import *

class bibli_scrap(bibli):

  def __init__(self, path):
    super().__init__(path)
    self.visited = set()  # Suivi des URLs déjà explorées
    
  def scrap(self,url,profondeur,nbmax,nbr_init=0):
    liens_html = [(url, profondeur)]  # File d'attente pour le scraping en largeur
    nbr = nbr_init

    while liens_html and nbr < nbmax:  # Continue tant qu'il reste des liens à explorer et des fichiers à télécharger
      url_actuel, prof_actuel = liens_html.pop(0)
            
      if url_actuel in self.visited:
        continue  # Ignore les URLs déjà visitées

      self.visited.add(url_actuel)  # Marque comme visité

      try:
        # Récupére le contenu de la page
        response = requests.get(url_actuel, verify=False, timeout=10)
        response.raise_for_status()
        contenu_html = response.text
      except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'accès à {url_actuel} : {e}")
        continue

      # Analyse du contenu HTML
      analyse = BeautifulSoup(contenu_html, 'html.parser')
      liens = analyse.find_all('a')

      if len(liens) == 0:
        print(f"Aucun lien trouvé sur la page {url_actuel}")
        continue

      for lien_init in liens:
        href = lien_init.get('href')
        if not href:
          continue  # Ignore les liens sans href
                
        lien = urljoin(url_actuel, href)

        if lien in self.visited:
          continue  # Ignore les liens déjà visités
                
        try:
          if lien.lower().endswith('.pdf'):
            livre = PDF(lien)
            self.ajouter(livre)
            nbr += 1
            if nbr >= nbmax:  # Arrête si le nombre maximum de fichiers est atteint
              break
          elif lien.lower().endswith('.epub'):
            livre = EPUB(lien)
            self.ajouter(livre)
            nbr += 1
            if nbr >= nbmax:  # Arrête si le nombre maximum de fichiers est atteint
              break
          elif "/" in href and "~" not in href and prof_actuel > 1:
            liens_html.append((lien, prof_actuel - 1))  # pour une future potentielle exploration
        except Exception as e:
          print(f"Erreur lors du traitement du lien {lien} : {e}")

    return f"{nbr} livres ajoutés"

if __name__ == "__main__":

  b=bibli_scrap('bibliotheque_test')
  b.scrap('https://math.univ-angers.fr/~jaclin/biblio/livres/',3,15)

  b.rapport_livres("EPUB", "rapport_scrap_livres.epub")
  b.rapport_auteurs("EPUB", "rapport_scrap_auteurs.epub")

  b.rapport_livres("PDF", "rapport_scrap_livres.pdf")
  b.rapport_auteurs("PDF", "rapport_scrap_auteurs.pdf")
