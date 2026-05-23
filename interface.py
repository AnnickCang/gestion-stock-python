import os
from datetime import datetime

import types_structure
import constantes as const
from gestion_stock import trouver_produit


CLE_NOM = const.CLE_NOM
CLE_QUANTITE = const.CLE_QUANTITE
CLE_SEUIL = const.CLE_SEUIL
CLE_PRIX = const.CLE_PRIX
LARGEUR_COL = const.LARGEUR_COL
LARGEUR_CADRE = const.LARGEUR_CADRE
LARGEUR_CADRE_INVENTAIRE = const.LARGEUR_CADRE_INVENTAIRE
TIRET_CADRE = const.TIRET_CADRE


def _afficher_separateur() -> None:
    print()


def _afficher_bordure_cadre(largeur_cadre: int) -> None:
    print(TIRET_CADRE * largeur_cadre)


def _afficher_stock_vide() -> None:
    print(const.INFO_STOCK_VIDE)


def _attendre_entree_utilisateur() -> None:
    input(const.NAV_MSG_ENTREE_POUR_CONTINUER)


def _attendre_entree_retour_menu() -> None:
    input(const.NAV_MSG_TOUCHE_ENTREE_RETOUR_MENU)


def _afficher_nom_colonnes_stock_et_alertes() -> None:
    _afficher_bordure_cadre(LARGEUR_CADRE)
    print(f"| {const.COL_PRODUIT:{LARGEUR_COL}} "
          f"| {const.COL_QUANTITE:>{LARGEUR_COL}} "
          f"| {const.COL_SEUIL:>{LARGEUR_COL}} |"
    )
    _afficher_bordure_cadre(LARGEUR_CADRE)


def _afficher_nom_colonnes_inventaire() -> None:
    _afficher_bordure_cadre(LARGEUR_CADRE_INVENTAIRE)
    print(f"| {const.COL_PRODUIT:{LARGEUR_COL}} "
          f"| {const.COL_QUANTITE:>{LARGEUR_COL}} "
          f"| {const.COL_PRIX:>{LARGEUR_COL}} "
          f"| {const.COL_TOTAL:>{LARGEUR_COL}} |"
    )
    _afficher_bordure_cadre(LARGEUR_CADRE_INVENTAIRE)


def _demander_retour_menu() -> bool:
    while True:
        entree_utilisateur = input(const.QST_RETOUR_MENU_PRINCIPAL).strip()
        match entree_utilisateur.capitalize():
            case const.CTRL_REP_OUI:
                return True
            case const.CTRL_REP_NON:
                return False
        print(const.CTRL_REP_OUI_NON)


def _demander_entier(message: str) -> int | None:
    """Renvoie l'entrée utilisateur après l'avoir convertie en entier
    ou None (si champ vide avec validation retour au menu principal)"""
    while True:
        entree_utilisateur = input(message).strip()
        if not entree_utilisateur: 
            if _demander_retour_menu():
                return None
            continue

        try:
            valeur = int(entree_utilisateur)
            if valeur >= 0:
                return valeur
            print(const.CTRL_NB_POSITIF)
        except ValueError:
            print(const.CTRL_NB_VALIDE)


def _demander_flottant(message: str) -> float | None:
    """Renvoie l'entrée utilisateur après l'avoir convertie en float
    ou None (si champ vide avec validation retour au menu principal)"""
    while True:
        entree_utilisateur = input(message).strip()
        if not entree_utilisateur:
            if _demander_retour_menu():
                return None
            continue

        try:
            valeur = float(entree_utilisateur)
            if valeur >= 0:
                return valeur
            print(const.CTRL_PRIX_VALIDE)
        except ValueError:
            print(const.CTRL_NB_VALIDE)


def _afficher_titre_sous_menu(titre: str, largeur_cadre: int) -> None:
    print(f"{titre:^{largeur_cadre}}")


def _afficher_saisie_vide_retour_menu(largeur_cadre: int) -> None:
    print(f"{const.NAV_MSG_SAISIE_VIDE_RETOUR_MENU:^{largeur_cadre}}\n")


def effacer_ecran_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def demander_info_produit(
    stock: list[types_structure.Produit]
) -> types_structure.Produit | None:
    """Renvoie un dict Produit (valeurs saisies par l'utilisateur) 
    ou None si la saisie est annulée"""
    titre = const.TITRE_SMENU_AJOUT_MODIF
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE)
    _afficher_saisie_vide_retour_menu(LARGEUR_CADRE)
    
    nom = demander_nom_produit(const.LBL_NOM_PRODUIT)
    if nom is None:
        return None
    
    produit = trouver_produit(stock, nom)
    if produit is None:
        print(const.INFO_PRODUIT_AJOUTE.format(nom))
    else:
        infos_produit = const.INFO_PRODUIT.format(
            produit[CLE_NOM],
            produit[CLE_QUANTITE],
            produit[CLE_SEUIL],
            produit[CLE_PRIX]
        )
        print(const.INFO_VALEUR_ACTU, infos_produit, sep='')

    quantite = _demander_entier(const.LBL_QUANTITE_PRODUIT)
    if quantite is None:
        return None
    
    seuil = _demander_entier(const.LBL_SEUIL_PRODUIT)
    if seuil is None:
        return None
    
    prix = _demander_flottant(const.LBL_PRIX_PRODUIT)
    if prix is None:
        return None
    
    return {
        CLE_NOM: nom, 
        CLE_QUANTITE: quantite, 
        CLE_SEUIL: seuil, 
        CLE_PRIX: prix
    }


def demander_nom_produit(message: str) -> str | None:
    while True:
        nom: str = input(message).strip()
        if not nom:
            return None
        
        if len(nom) > LARGEUR_COL:
            print(const.CTRL_NOM_TROP_LONG.format(LARGEUR_COL))
            continue
        
        return nom


def demander_nouveau_nom(ancien_nom: str) -> str | None:
    nouveau_nom = demander_nom_produit(
        const.LBL_NOUVEAU_NOM_PRODUIT.format(ancien_nom)
    )
    if nouveau_nom is None:
        return None
    
    return nouveau_nom


def demander_confirmation_suppression(nom_produit: str) -> bool:
    while True:
        question = const.QST_SUPPRESSION.format(nom_produit)
        entree_utilisateur = input(question).strip()
        match entree_utilisateur.capitalize():
            case const.CTRL_REP_OUI:
                return True
            case const.CTRL_REP_NON:
                _afficher_separateur()
                return False
        _afficher_separateur()
        print(const.CTRL_REP_OUI_NON)
        _afficher_separateur()


def afficher_stock(stock: list[types_structure.Produit]) -> None:
    """Affiche le stock actuel avec quantités et seuils"""
    titre = const.TITRE_SMENU_STOCK
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE)
    
    if not stock:
        _afficher_stock_vide()
        _attendre_entree_retour_menu()
        return
    
    _afficher_nom_colonnes_stock_et_alertes()
    for produit in stock:
        print(f"| {produit[CLE_NOM]:{LARGEUR_COL}} "
              f"| {produit[CLE_QUANTITE]:>{LARGEUR_COL}} "
              f"| {produit[CLE_SEUIL]:>{LARGEUR_COL}} |"
        )
    _afficher_bordure_cadre(LARGEUR_CADRE)
    _attendre_entree_retour_menu()


def afficher_alertes(alertes: list[types_structure.Produit]) -> None:
    """Affiche la liste des noms de produits en dessous du seuil"""
    titre = const.TITRE_SMENU_ALERTES
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE)
    
    if not alertes:
        print(const.INFO_AUCUNE_ALERTE)
        _attendre_entree_retour_menu()
        return
    
    _afficher_nom_colonnes_stock_et_alertes()
    for produit in alertes:
        print(f"| {produit[CLE_NOM]:{LARGEUR_COL}} "
              f"| {produit[CLE_QUANTITE]:>{LARGEUR_COL}} "
              f"| {produit[CLE_SEUIL]:>{LARGEUR_COL}} |"
        )
    _afficher_bordure_cadre(LARGEUR_CADRE)
    _attendre_entree_retour_menu()


def afficher_info_produit(produit: types_structure.Produit) -> None:
    """Affiche les données relatives au produit recherché s'il a été trouvé"""
    print(
        const.INFO_PRODUIT.format(
            produit[CLE_NOM],
            produit[CLE_QUANTITE],
            produit[CLE_SEUIL],
            produit[CLE_PRIX])
    )
    _afficher_separateur()
        

def afficher_inventaire(stock: list[types_structure.Produit]) -> None:
    """Affiche les données relatives à chaque produit ainsi que le montant
    total pour chaque produit et le montant de la totalité du stock
    à la date du jour"""
    jour = datetime.today().strftime("%d/%m/%Y")
    titre = const.TITRE_SMENU_INVENTAIRE + jour + " ---"
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE_INVENTAIRE)
    
    if not stock:
        _afficher_stock_vide()
        _attendre_entree_retour_menu()
        return
    
    _afficher_nom_colonnes_inventaire()
    cout_total_stock = 0.0
    for produit in stock:
        cout_total_produit = produit[CLE_QUANTITE] * produit[CLE_PRIX]
        print(f"| {produit[CLE_NOM]:{LARGEUR_COL}} "
              f"| {produit[CLE_QUANTITE]:>{LARGEUR_COL}} "
              f"| {produit[CLE_PRIX]:>{LARGEUR_COL}.2f} "
              f"| {cout_total_produit:>{LARGEUR_COL}.2f} |"
        )
        cout_total_stock += cout_total_produit
    _afficher_bordure_cadre(LARGEUR_CADRE_INVENTAIRE)
    texte_total_stock = const.INFO_COUT_STOCK.format(cout_total_stock)
    print(f"\n{texte_total_stock:>{LARGEUR_CADRE_INVENTAIRE}}")
    _attendre_entree_retour_menu()


def afficher_erreur(code_err: int) -> None:
    match code_err:
        case const.ERR_FILE_NOT_FOUND:
            print(const.ERR_MSG_FICHIER_STOCK_ABSENT)
        case const.ERR_JSON_DECODE_ERROR:
            print(const.ERR_MSG_FICHIER_STOCK_ENDOMMAGE)
            print(const.ERR_MSG_NOUVEAU_FICHIER_STOCK)
            print(const.ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE)
        case const.ERR_STOCK_PAS_UNE_LISTE:
            print(const.ERR_MSG_FICHIER_MAUVAISE_STRUCTURE)
            print(const.ERR_MSG_FICHIER_STRUCTURE_LISTE_OBLIGATOIRE)
            print(const.ERR_MSG_NOUVEAU_FICHIER_STOCK)
            print(const.ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE)
    _attendre_entree_utilisateur()


def afficher_anomalies_fichier(anomalies: list[str]) -> None:
    print(const.ANO_LISTE)
    for anomalie in anomalies:
        print(anomalie)
    print(const.ANO_MSG_NOUVEAU_FICHIER_STOCK)
    print(const.ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE)
    _attendre_entree_utilisateur()


def demander_choix_menu() -> str:
    """Affiche le menu principal et renvoie le choix de l'utilisateur"""

    print(f"{const.TITRE_MENU_PRINCIPAL:^{LARGEUR_CADRE}}\n")
    print(const.MENUP_SM_STOCK)
    print(const.MENUP_SM_ALERTES)
    print(const.MENUP_SM_AJOUT_MODIF)
    print(const.MENUP_SM_SUPPRESSION)
    print(const.MENUP_SM_RECHERCHE)
    print(const.MENUP_SM_RENOMMAGE)
    print(const.MENUP_SM_INVENTAIRE)
    print(const.MENUP_SM_QUITTER)

    choix = input(const.MENUP_CHOIX).strip()
    while choix not in const.LISTE_CHOIX:
        choix = input(const.MENUP_REPETER_CHOIX).strip()
    
    return choix


def afficher_produit_ajoute() -> None:
    print(const.INFO_PROD_AJOUTE)
    _afficher_separateur()


def afficher_produit_modifie() -> None:
    print(const.INFO_PROD_MODIFIE)
    _afficher_separateur()


def afficher_produit_non_trouve() -> None:
    print(const.INFO_PROD_NON_TROUVE)
    _afficher_separateur()


def afficher_produit_supprime(nom_produit: str) -> None:
    print(const.INFO_PROD_SUPPRIME.format(nom_produit))
    _afficher_separateur()


def afficher_produit_renomme(ancien_nom: str, nouveau_nom: str) -> None:
    print(const.INFO_PROD_RENOMME.format(ancien_nom, nouveau_nom))
    _afficher_separateur()


def afficher_produit_existe(nom: str) -> None:
    print(const.CTRL_NOM_EXISTE_DEJA.format(nom))


def afficher_suggestions(suggestions: list[str]) -> None:
    """Affiche une liste de suggestions pour la recherche d'un produit"""
    print(const.RECH_SUGGESTIONS)
    for suggestion in suggestions:
        print(const.RECH_NOM_SUGGERE.format(suggestion))
    _afficher_separateur()


def afficher_recherche_impossible() -> None:
    print(const.INFO_RECHERCHE_STOCK_VIDE)
    _attendre_entree_retour_menu()


def afficher_suppression_impossible() -> None:
    print(const.INFO_SUPPRESSION_STOCK_VIDE)
    _attendre_entree_retour_menu()


def afficher_renommage_impossible() -> None:
    print(const.INFO_RENOMMAGE_STOCK_VIDE)
    _attendre_entree_retour_menu()


def afficher_entete_suppression() -> None:
    titre = const.TITRE_SMENU_SUPPRESSION
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE)
    _afficher_saisie_vide_retour_menu(LARGEUR_CADRE)


def afficher_entete_recherche() -> None:
    titre = const.TITRE_SMENU_RECHERCHE
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE)
    _afficher_saisie_vide_retour_menu(LARGEUR_CADRE)


def afficher_entete_renommage() -> None:
    titre = const.TITRE_SMENU_RENOMMAGE
    _afficher_titre_sous_menu(titre, LARGEUR_CADRE)
    _afficher_saisie_vide_retour_menu(LARGEUR_CADRE)