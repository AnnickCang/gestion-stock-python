import json

import types_structure
import constantes as const
from normalisation import normaliser_chaine_pour_comparaison as norm


CLE_NOM = const.CLE_NOM
CLE_QUANTITE = const.CLE_QUANTITE
CLE_SEUIL = const.CLE_SEUIL
CLE_PRIX = const.CLE_PRIX


def trier_stock(stock: list[types_structure.Produit]) -> None:
    """Trie le stock par nom de produit"""
    stock.sort(key=lambda item: norm(item[CLE_NOM]))


def _verifier_structure_stock(stock: object) -> int:
    """Renvoie un code indiquant si la structure est valide ou pas"""
    if not isinstance(stock, list):
        return const.ERR_STOCK_PAS_UNE_LISTE
    
    return const.NO_ERR


def _extraire_champ_entier_valide(
    produit: dict[str, object],
    champ: str
) -> tuple[int, str]:
    """Vérifie et renvoie un entier >= 0 avec éventuellement un warning"""

    entier_valide = 0

    msg_champ_inexistant = const.ANO_CHAMP_NUM_INEXISTANT.format(champ)
    msg_converti_a_zero = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
    msg_converti_en_entier = const.ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT.format(
        champ,
        const.ANO_ENTIER
    )

    if champ not in produit:
        return entier_valide, msg_champ_inexistant
    
    valeur_champ = produit[champ]

    if isinstance(valeur_champ, int):
        if isinstance(valeur_champ, bool) or valeur_champ < 0:
            return entier_valide, msg_converti_a_zero
        
        valeur = valeur_champ
        return valeur, ""
    
    if isinstance(valeur_champ, float):
        if valeur_champ < 0:
            return entier_valide, msg_converti_a_zero
        
        entier_valide = int(valeur_champ)
        return entier_valide, msg_converti_en_entier
    
    if isinstance(valeur_champ, str):
        try:
            valeur_convertie = float(valeur_champ)
            valeur_convertie = int(valeur_convertie)

            if valeur_convertie < 0:
                return entier_valide, msg_converti_a_zero

            entier_valide = valeur_convertie
            msg_converti_en_nombre = const.ANO_CHAMP_NUM_CONV_VAL.format(
                champ,
                entier_valide
            )
            return entier_valide, msg_converti_en_nombre

        except ValueError:
            return entier_valide, msg_converti_a_zero

    return entier_valide, msg_converti_a_zero


def _extraire_champ_flottant_valide(
    produit: dict[str, object],
    champ: str
) -> tuple[float, str]:
    """Vérifie et renvoie un flottant >= 0 avec éventuellement un warning"""

    flottant_valide = 0.0

    msg_champ_inexistant = const.ANO_CHAMP_NUM_INEXISTANT.format(champ)
    msg_converti_a_zero = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
    msg_converti_en_flottant = const.ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT.format(
        champ,
        const.ANO_FLOTTANT
    )

    if champ not in produit:
        return flottant_valide, msg_champ_inexistant
    
    valeur_champ = produit[champ]

    if isinstance(valeur_champ, float):
        if valeur_champ < 0:
            return flottant_valide, msg_converti_a_zero
        
        flottant_valide = valeur_champ
        return flottant_valide, ""
    
    if isinstance(valeur_champ, int):
        if isinstance(valeur_champ, bool) or valeur_champ < 0:
            return flottant_valide, msg_converti_a_zero
        
        flottant_valide = float(valeur_champ)
        return flottant_valide, msg_converti_en_flottant
    
    if isinstance(valeur_champ, str):
        try:
            valeur_convertie = float(valeur_champ)

            if valeur_convertie < 0:
                return flottant_valide, msg_converti_a_zero

            flottant_valide = valeur_convertie
            msg_converti_en_nombre = const.ANO_CHAMP_NUM_CONV_VAL.format(
                champ,
                flottant_valide
            )
            return flottant_valide, msg_converti_en_nombre

        except ValueError:
            return flottant_valide, msg_converti_a_zero
    
    return flottant_valide, msg_converti_a_zero


def _extraire_nom_produit_valide(
    produit: dict[str, object]
) -> tuple[str | None, list[str]]:
    """Vérifie et renvoie un nom valide ou None avec la liste des warnings associés"""
    
    largeur_colonne = const.LARGEUR_COL

    anomalies_nom = []
    
    if CLE_NOM not in produit:
        anomalies_nom.append(const.ANO_NOM_INEXISTANT)
        return None, anomalies_nom
    
    nom = produit[CLE_NOM]
    if not isinstance(nom, str):
        anomalies_nom.append(const.ANO_CHAMP_PAS_STR.format(CLE_NOM))
        return None, anomalies_nom
    
    nom_strip = nom.strip()
    if nom_strip == "":
        anomalies_nom.append(const.ANO_NOM_VIDE.format(CLE_NOM))
        return None, anomalies_nom
        
    if len(nom_strip) > largeur_colonne:
        nom_strip = nom_strip[:largeur_colonne]
        anomalies_nom.append(
            const.ANO_CHAMP_TROP_LONG.format(CLE_NOM, largeur_colonne)
        )
    
    return nom_strip, anomalies_nom


def _extraire_champs_numeriques_valides(
    produit: dict[str, object]
) -> tuple[types_structure.ChampsNumeriquesProduit, list[str]]:
    """Vérifie et renvoie les champs numériques avec une valeur valide ou 0
    et la liste des warnings associés"""
    
    champs_numeriques_anomalies = []

    quantite, msg_anomalie = _extraire_champ_entier_valide(produit, CLE_QUANTITE)
    if msg_anomalie != "":
        champs_numeriques_anomalies.append(msg_anomalie)
    seuil, msg_anomalie = _extraire_champ_entier_valide(produit, CLE_SEUIL)
    if msg_anomalie != "":
        champs_numeriques_anomalies.append(msg_anomalie)
    prix, msg_anomalie = _extraire_champ_flottant_valide(produit, CLE_PRIX)
    if msg_anomalie != "":
        champs_numeriques_anomalies.append(msg_anomalie)

    champs_numeriques_produit: types_structure.ChampsNumeriquesProduit = {
        CLE_QUANTITE: quantite,
        CLE_SEUIL: seuil,
        CLE_PRIX: prix
    }
    return champs_numeriques_produit, champs_numeriques_anomalies


def _extraire_produit_valide(
    produit: object
) -> tuple[types_structure.Produit | None, list[str]]:
    """Vérifie et retourne un produit avec des clés et valeurs valides ou None
    et la liste de warnings associés"""
    
    produit_anomalies = []

    if not isinstance(produit, dict):
        produit_anomalies.append(const.ANO_PRODUIT_STRUCTURE_INVALIDE)
        return None, produit_anomalies
     
    produit_dict: dict[str, object] = produit
    nom_nettoye, nom_anomalies = _extraire_nom_produit_valide(produit_dict)
    produit_anomalies.extend(nom_anomalies)
    if nom_nettoye is None:
        return None, produit_anomalies
    
    numeriques_valides, anomalies_numeriques = _extraire_champs_numeriques_valides(produit_dict)
    produit_anomalies.extend(anomalies_numeriques)
    
    produit_nettoye: types_structure.Produit = {
        CLE_NOM: nom_nettoye,
        CLE_QUANTITE: numeriques_valides[CLE_QUANTITE],
        CLE_SEUIL: numeriques_valides[CLE_SEUIL],
        CLE_PRIX: numeriques_valides[CLE_PRIX]
    }
    return produit_nettoye, produit_anomalies


def _extraire_stock_valide(
    stock: list[object]
) -> tuple[list[types_structure.Produit], list[str]]:
    """Renvoie un stock avec des produits vérifiés, nettoyés et sans doublons
    et éventuellement les anomalies associées"""

    stock_nettoye: list[types_structure.Produit] = []
    anomalies: list[str] = []
    cles_noms_deja_vus: set[str] = set()

    for no_produit, produit in enumerate(stock, start=1):
        produit_nettoye, msgs_anomalies = _extraire_produit_valide(produit)
        
        if produit_nettoye is not None:
            nom_normalise = norm(produit_nettoye[CLE_NOM])
            if nom_normalise in cles_noms_deja_vus:
                msg_anomalie = const.ANO_NOM_DOUBLON.format(produit_nettoye[CLE_NOM])
                msgs_anomalies.append(msg_anomalie)
            else:
                cles_noms_deja_vus.add(nom_normalise)
                stock_nettoye.append(produit_nettoye)
        
        for anomalie in msgs_anomalies:
            txt_anomalie = const.ANO_NO_PRODUIT.format(no_produit)
            anomalies.append(txt_anomalie + anomalie)
    
    return stock_nettoye, anomalies


def charger_stock() -> tuple[int, list[types_structure.Produit], list[str]]:
    """Charge les données du fichier de stock et renvoie le code erreur ou pas d'erreur,
    la liste des produits valides et la liste des anomalies"""
    try:
        with open(const.FICHIER_STOCK, "r", encoding="utf-8") as f:
            stock = json.load(f)

            if _verifier_structure_stock(stock) == const.ERR_STOCK_PAS_UNE_LISTE:
                return const.ERR_STOCK_PAS_UNE_LISTE, [], []

            stock_nettoye, anomalies = _extraire_stock_valide(stock)

            trier_stock(stock_nettoye)

            return const.NO_ERR, stock_nettoye, anomalies
        
    except FileNotFoundError:
        return const.ERR_FILE_NOT_FOUND, [], []
    except json.JSONDecodeError:
        return const.ERR_JSON_DECODE_ERROR, [], []
    
    
def sauvegarder_stock(stock: list[types_structure.Produit]) -> None:
    """Sauvegarde le stock trié par nom"""
    trier_stock(stock)
    with open(const.FICHIER_STOCK, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)