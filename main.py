from datetime import datetime

import constantes as const
import interface as ifc
import gestion_stock as gs
import donnees

def main():
    code_err, stock, anomalies_fichier = donnees.charger_stock()

    if code_err != const.NO_ERR:
        ifc.afficher_erreur(code_err)
    
    if anomalies_fichier:
        ifc.afficher_anomalies_fichier(anomalies_fichier)

    continuer = True
    while continuer:
        ifc.effacer_ecran_terminal()
        choix = ifc.demander_choix_menu()

        ifc.effacer_ecran_terminal()
        match choix.capitalize():
            case const.MENUP_CHOIX_STOCK:
                ifc.afficher_titre_sous_menu(const.TITRE_SMENU_STOCK)
                ifc.afficher_stock(stock)
            case const.MENUP_CHOIX_ALERTES:
                 ifc.afficher_titre_sous_menu(
                     const.TITRE_SMENU_ALERTES)
                 alertes = gs.trouver_alertes(stock)
                 ifc.afficher_alertes(alertes)
            case const.MENUP_CHOIX_AJOUT_MODIF:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_AJOUT_MODIF, True)
                    donnees_produit =  ifc.demander_info_produit(stock)
                    if donnees_produit is None:
                        break
                    else:
                        if gs.ajouter_ou_modifier_produit(stock, 
                                                          **donnees_produit
                        ) == const.RETOUR_AJOUT:
                            ifc.afficher_produit_ajoute()
                        else:
                            ifc.afficher_produit_modifie()
            case const.MENUP_CHOIX_SUPPRESSION:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_SUPPRESSION, 
                        True
                    )
                    nom_prod = ifc.demander_nom_produit(const.LBL_NOM_PRODUIT)
                    if nom_prod:
                        prod = gs.trouver_produit(stock, nom_prod)
                        if prod is None:
                            ifc.afficher_produit_non_trouve()
                        else:
                            if ifc.demander_confirmation_suppression():
                                gs.supprimer_produit(stock, prod)
                                ifc.afficher_produit_supprime(
                                    prod[const.CLE_NOM]
                                )
                    else:
                        break
            case const.MENUP_CHOIX_RECHERCHE:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_RECHERCHE, 
                        True
                    )
                    nom_prod = ifc.demander_nom_produit(const.LBL_NOM_PRODUIT)
                    if nom_prod:
                        prod = gs.trouver_produit(stock, nom_prod)
                        ifc.afficher_info_produit(prod)
                    else:
                        break
            case const.MENUP_CHOIX_RENOMMAGE:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_RENOMMAGE, 
                        True
                    )
                    nom_prod = ifc.demander_nom_produit(const.LBL_NOM_PRODUIT)
                    if nom_prod is None:
                        break
                        
                    prod = gs.trouver_produit(stock, nom_prod)
                    if prod is None:
                        ifc.afficher_produit_non_trouve()
                    else:
                        retour_menu = False
                        while True:
                            nouveau_nom = ifc.demander_nouveau_nom()
                            if nouveau_nom is None:
                                retour_menu = True
                                break
                                
                            if gs.verifier_nom_disponible(
                                stock, prod[const.CLE_NOM], nouveau_nom
                            ):
                                ancien_nom = prod[const.CLE_NOM]
                                gs.renommer_produit(stock, prod, nouveau_nom)
                                ifc.afficher_produit_renomme(ancien_nom, nouveau_nom)
                                break
                                
                            ifc.afficher_produit_existe(nouveau_nom)
                        
                        if retour_menu:
                            break
            case const.MENUP_CHOIX_INVENTAIRE:
                jour = datetime.today().strftime("%d/%m/%Y")
                titre = const.TITRE_SMENU_INVENTAIRE + jour + " ---"
                ifc.afficher_titre_sous_menu(titre, pour_inventaire=True)
                ifc.afficher_inventaire(stock)
            case const.MENUP_CHOIX_QUITTER:
                continuer = False                

if __name__ == "__main__":
    main()