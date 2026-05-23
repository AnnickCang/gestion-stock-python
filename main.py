from datetime import datetime

import types_structure
import constantes as const
import interface as ifc
import gestion_stock as gs
import donnees
import suggestions_produits as sp


LARGEUR_CADRE = const.LARGEUR_CADRE
LBL_NOM_PRODUIT = const.LBL_NOM_PRODUIT
CLE_NOM = const.CLE_NOM


def _gerer_ajout_modification(stock: list[types_structure.Produit]) -> None:
    while True:
        titre = const.TITRE_SMENU_AJOUT_MODIF
        ifc.afficher_titre_sous_menu(titre, LARGEUR_CADRE)
        ifc.afficher_saisie_vide_retour_menu(LARGEUR_CADRE)
        donnees_produit = ifc.demander_info_produit(stock)
        if donnees_produit is None:
            break
        
        action_effectuee = gs.ajouter_ou_modifier_produit(
            stock,
            **donnees_produit
        )

        if action_effectuee == const.RETOUR_AJOUT:
            ifc.afficher_produit_ajoute()
            continue

        ifc.afficher_produit_modifie()


def _gerer_suppression(stock: list[types_structure.Produit]) -> None:
    while True:
        titre = const.TITRE_SMENU_SUPPRESSION
        ifc.afficher_titre_sous_menu(titre, LARGEUR_CADRE)
        ifc.afficher_saisie_vide_retour_menu(LARGEUR_CADRE)

        if not stock:
            ifc.afficher_suppression_impossible()
            break

        nom_produit = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_produit is None:
            break
        
        produit = gs.trouver_produit(stock, nom_produit)
        if produit is None:
            ifc.afficher_produit_non_trouve()
            continue

        nom_produit_a_supprimer = produit[CLE_NOM]
        if ifc.demander_confirmation_suppression(nom_produit_a_supprimer):
            gs.supprimer_produit(stock, produit)
            ifc.afficher_produit_supprime(nom_produit_a_supprimer)


def _gerer_recherche(stock: list[types_structure.Produit]) -> None:
    while True:
        titre = const.TITRE_SMENU_RECHERCHE
        ifc.afficher_titre_sous_menu(titre, LARGEUR_CADRE)
        ifc.afficher_saisie_vide_retour_menu(LARGEUR_CADRE)

        if not stock:
            ifc.afficher_recherche_impossible()
            break

        nom_recherche = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_recherche is None:
            break
        
        produit = gs.trouver_produit(stock, nom_recherche)
        if produit is not None:
            ifc.afficher_info_produit(produit)
            continue

        suggestions = sp.suggerer_produits(stock, nom_recherche)
        if suggestions:
            ifc.afficher_suggestions(suggestions)
            continue

        ifc.afficher_produit_non_trouve()


def _gerer_renommage(stock: list[types_structure.Produit]) -> None:
    while True:
        titre = const.TITRE_SMENU_RENOMMAGE
        ifc.afficher_titre_sous_menu(titre, LARGEUR_CADRE)
        ifc.afficher_saisie_vide_retour_menu(LARGEUR_CADRE)

        if not stock:
            ifc.afficher_renommage_impossible()
            break

        nom_produit = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_produit is None:
            break
        
        produit = gs.trouver_produit(stock, nom_produit)
        if produit is None:
            ifc.afficher_produit_non_trouve()
            continue

        retour_menu_principal = False
        while True:
            ancien_nom = produit[CLE_NOM]
            nouveau_nom = ifc.demander_nouveau_nom(ancien_nom)
            if nouveau_nom is None:
                retour_menu_principal = True
                break
                
            if gs.verifier_nom_disponible(
                stock, produit[CLE_NOM], nouveau_nom
            ):
                gs.renommer_produit(stock, produit, nouveau_nom)
                ifc.afficher_produit_renomme(ancien_nom, nouveau_nom)
                break
                
            ifc.afficher_produit_existe(nouveau_nom)
        
        if retour_menu_principal:
            break


def main():
    code_err, stock, anomalies_du_fichier = donnees.charger_stock()

    if code_err != const.NO_ERR:
        ifc.afficher_erreur(code_err)
    
    if anomalies_du_fichier:
        ifc.afficher_anomalies_fichier(anomalies_du_fichier)

    continuer = True
    while continuer:
        ifc.effacer_ecran_terminal()
        choix_menu = ifc.demander_choix_menu()

        ifc.effacer_ecran_terminal()
        match choix_menu.capitalize():
            case const.MENUP_CHOIX_STOCK:
                titre = const.TITRE_SMENU_STOCK
                ifc.afficher_titre_sous_menu(titre, LARGEUR_CADRE)
                ifc.afficher_stock(stock)

            case const.MENUP_CHOIX_ALERTES:
                titre = const.TITRE_SMENU_ALERTES
                ifc.afficher_titre_sous_menu(titre, LARGEUR_CADRE)
                alertes = gs.trouver_alertes(stock)
                ifc.afficher_alertes(alertes)

            case const.MENUP_CHOIX_AJOUT_MODIF:
                _gerer_ajout_modification(stock)

            case const.MENUP_CHOIX_SUPPRESSION:
                _gerer_suppression(stock)

            case const.MENUP_CHOIX_RECHERCHE:
                _gerer_recherche(stock)

            case const.MENUP_CHOIX_RENOMMAGE:
                _gerer_renommage(stock)

            case const.MENUP_CHOIX_INVENTAIRE:
                jour = datetime.today().strftime("%d/%m/%Y")
                titre = const.TITRE_SMENU_INVENTAIRE + jour + " ---"
                ifc.afficher_titre_sous_menu(titre, const.LARGEUR_CADRE_INVENTAIRE)
                ifc.afficher_inventaire(stock)

            case const.MENUP_CHOIX_QUITTER:
                continuer = False


if __name__ == "__main__":
    main()