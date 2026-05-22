import unicodedata


def normaliser_chaine_pour_comparaison(chaine: str) -> str:
    """Renvoie une chaîne en minuscule et sans les accents"""
    chaine_retour = unicodedata.normalize('NFD', chaine.lower())
    chaine_retour = ''.join(
        caractere for caractere in chaine_retour
        if unicodedata.category(caractere) != 'Mn'
    )
    return chaine_retour