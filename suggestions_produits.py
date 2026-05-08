from difflib import get_close_matches

import types_structure
import constantes as const
from normalisation import normaliser_chaine_pour_comparaison as norm

def suggerer_produits(stock: list[types_structure.Produit],
                      nom_recherche: str
)-> list[str]:
    """Renvoie les noms de produits proche du nom recherché"""
    noms_normalises = []
    correspondance_entre_noms = {}
    suggestions_noms_reels = []

    for prod in stock:
        nom_normalise = norm(prod[const.CLE_NOM])
        nom_reel = prod[const.CLE_NOM]
        noms_normalises.append(nom_normalise)
        correspondance_entre_noms[nom_normalise] = nom_reel

    suggestions = get_close_matches(norm(nom_recherche), 
                                    noms_normalises, 
                                    const.RECH_NB_ELEMENTS_RETOUR, 
                                    const.RECH_SEUIL_SIMILARITE
                                    )
    
    for nom_normalise in suggestions:
        suggestions_noms_reels.append(
            correspondance_entre_noms[nom_normalise]
        )
    
    return suggestions_noms_reels