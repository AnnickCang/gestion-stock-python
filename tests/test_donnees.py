import pytest

from constantes_tests import CLE_NOM, CLE_PRIX, CLE_QUANTITE, CLE_SEUIL
import donnees

MSG_CONVERTI_A_ZERO = (
    f"Le champ '{CLE_QUANTITE}' a été converti en nombre avec une valeur à 0."
)
MSG_CHAMP_INEXISTANT = (
    f"Le champ '{CLE_QUANTITE}' n'existe pas et a été créé avec une valeur à 0."
)
MSG_CONVERTI_EN_ENTIER = (
    f"Le champ '{CLE_QUANTITE}' a été converti en 'int', sa valeur peut être tronquée."
)

@pytest.mark.parametrize(
    ("objet_teste", "resultat_attendu"),
    [
        (
            [1, 2, 3],
            donnees.ResultatChargementFichier.SUCCES),
        (
            {CLE_NOM: "coco", CLE_QUANTITE: 2},
            donnees.ResultatChargementFichier.STOCK_PAS_UNE_LISTE
         ),
    ]
)


def test__verifier_structure_stock(objet_teste, resultat_attendu):
    resultat = donnees._verifier_structure_stock(objet_teste)

    assert resultat == resultat_attendu


@pytest.mark.parametrize(
    ("produit", "valeur_attendue", "warning_attendu"),
    [
        (
            {CLE_NOM: "banane", CLE_QUANTITE: 1, CLE_SEUIL: 3, CLE_PRIX: 0.5},
            1,
            ""
        ),
        (
            {CLE_NOM: "banane", CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CHAMP_INEXISTANT
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: True, CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CONVERTI_A_ZERO
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: -5, CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CONVERTI_A_ZERO
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: -1.5, CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CONVERTI_A_ZERO
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: 2.7, CLE_SEUIL: 3, CLE_PRIX: 0.5},
            2,
            MSG_CONVERTI_EN_ENTIER
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: "oups", CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CONVERTI_A_ZERO
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: "-5.2", CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CONVERTI_A_ZERO
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: "3.8", CLE_SEUIL: 3, CLE_PRIX: 0.5},
            3,
            f"Le champ '{CLE_QUANTITE}' a été converti en nombre avec la valeur '3'."
        ),
        (
            {CLE_NOM: "banane", CLE_QUANTITE: [1, 2, 3], CLE_SEUIL: 3, CLE_PRIX: 0.5},
            0,
            MSG_CONVERTI_A_ZERO
        ),
    ]
)


def test__extraire_champ_entier_valide(produit, valeur_attendue, warning_attendu):
    champ_teste = CLE_QUANTITE

    valeur, warning = donnees._extraire_champ_entier_valide(produit, champ_teste)

    assert valeur == valeur_attendue
    assert warning == warning_attendu