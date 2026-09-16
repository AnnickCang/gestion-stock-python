import pytest

from constantes_tests import CLE_NOM, CLE_PRIX, CLE_QUANTITE, CLE_SEUIL
import gestion_stock
import types_structure


@pytest.mark.parametrize(
    ("nom_recherche", "produit_attendu"),
    [
        ("banane", None),
        ("café", {CLE_NOM: "Café", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 18.5}),
        ("cafe", {CLE_NOM: "Café", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 18.5}),
    ],
)


def test_trouver_produit(nom_recherche, produit_attendu):
    stock: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 15, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "Café", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 18.5},
        {CLE_NOM: "CHOCOLAT", CLE_QUANTITE: 1, CLE_SEUIL: 2, CLE_PRIX: 3.75},
        {CLE_NOM: "M&M's", CLE_QUANTITE: 10, CLE_SEUIL: 3, CLE_PRIX: 2.5},
        {CLE_NOM: "Tomate cerise", CLE_QUANTITE: 5, CLE_SEUIL: 10, CLE_PRIX: 0.75},
    ]

    resultat = gestion_stock.trouver_produit(stock, nom_recherche)

    assert resultat == produit_attendu


def test_ajouter_produit():
    stock: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 15, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "Café", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 18.5},
    ]
    stock_attendu: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 15, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "Café", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 18.5},
        {CLE_NOM: "CHOCOLAT", CLE_QUANTITE: 1, CLE_SEUIL: 2, CLE_PRIX: 3.75},
    ]
    nom = "CHOCOLAT"
    quantite = 1
    seuil = 2
    prix = 3.749

    gestion_stock.ajouter_produit(stock, nom, quantite, seuil, prix)

    assert stock == stock_attendu


def test_modifier_produit():
    produit_a_modifier: types_structure.Produit = {
        CLE_NOM: "CHOCOLAT",
        CLE_QUANTITE: 1,
        CLE_SEUIL: 2,
        CLE_PRIX: 3.75
    }
    nouvelle_quantite = 5
    nouveau_seuil = 3
    nouveau_prix = 2.233
    produit_attendu: types_structure.Produit = {
        CLE_NOM: "CHOCOLAT",
        CLE_QUANTITE: 5,
        CLE_SEUIL: 3,
        CLE_PRIX: 2.23
    }

    gestion_stock.modifier_produit(
        produit_a_modifier,
        nouvelle_quantite,
        nouveau_seuil,
        nouveau_prix
    )

    assert produit_a_modifier == produit_attendu


def test_trouver_alertes():
    stock: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 5, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "Café", CLE_QUANTITE: 1, CLE_SEUIL: 2, CLE_PRIX: 18.5},
        {CLE_NOM: "CHOCOLAT", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 3.75},
        {CLE_NOM: "M&M's", CLE_QUANTITE: 10, CLE_SEUIL: 3, CLE_PRIX: 2.5},
        {CLE_NOM: "noix de Cajou", CLE_QUANTITE: 10, CLE_SEUIL: 10, CLE_PRIX: 0.75},
        {CLE_NOM: "Tomate cerise", CLE_QUANTITE: 5, CLE_SEUIL: 10, CLE_PRIX: 0.75},
    ]
    alertes_attendues: list[types_structure.Produit] = [
        {CLE_NOM: "Café", CLE_QUANTITE: 1, CLE_SEUIL: 2, CLE_PRIX: 18.5},
        {CLE_NOM: "Tomate cerise", CLE_QUANTITE: 5, CLE_SEUIL: 10, CLE_PRIX: 0.75},
    ]

    resultat = gestion_stock.trouver_alertes(stock)

    assert resultat == alertes_attendues


def test_supprimer_produit():
    stock: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 5, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "Café", CLE_QUANTITE: 1, CLE_SEUIL: 2, CLE_PRIX: 18.5},
        {CLE_NOM: "CHOCOLAT", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 3.75},
    ]
    produit_a_supprimer: types_structure.Produit = {
        CLE_NOM: "Café",
        CLE_QUANTITE: 1,
        CLE_SEUIL: 2,
        CLE_PRIX: 18.5
    }
    stock_attendu: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 5, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "CHOCOLAT", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 3.75},
    ]

    gestion_stock.supprimer_produit(stock, produit_a_supprimer)

    assert stock == stock_attendu


def test_renommer_produit():
    produit: types_structure.Produit = {
        CLE_NOM: "Café",
        CLE_QUANTITE: 1,
        CLE_SEUIL: 2,
        CLE_PRIX: 18.5
    }
    nouveau_nom = "Décaféiné"
    produit_attendu: types_structure.Produit = {
        CLE_NOM: "Décaféiné",
        CLE_QUANTITE: 1,
        CLE_SEUIL: 2,
        CLE_PRIX: 18.5
    }

    gestion_stock.renommer_produit(produit, nouveau_nom)

    assert produit == produit_attendu


@pytest.mark.parametrize(
    ("ancien_nom", "nouveau_nom", "booleen_attendu"),
    [
        ("Café", "Bonbon", False),
        ("deca", "Déca", True),
        ("bonbon", "chocolat", True),
    ]
)


def test_verifier_nom_disponible(ancien_nom, nouveau_nom, booleen_attendu):
    stock: list[types_structure.Produit] = [
        {CLE_NOM: "bonbon", CLE_QUANTITE: 5, CLE_SEUIL: 5, CLE_PRIX: 0.5},
        {CLE_NOM: "Café", CLE_QUANTITE: 1, CLE_SEUIL: 2, CLE_PRIX: 18.5},
        {CLE_NOM: "deca", CLE_QUANTITE: 3, CLE_SEUIL: 2, CLE_PRIX: 15.0},
    ]
    resultat = gestion_stock.verifier_nom_disponible(stock, ancien_nom, nouveau_nom)

    assert resultat == booleen_attendu


@pytest.mark.parametrize(
    ("produit", "booleen_attendu"),
    [
        ({CLE_NOM: "Banane", CLE_QUANTITE: 3, CLE_SEUIL: 5, CLE_PRIX: 0.35}, True),
        ({CLE_NOM: "Coco", CLE_QUANTITE: 3, CLE_SEUIL: 1, CLE_PRIX: 1.5}, False),
        ({CLE_NOM: "Fraise", CLE_QUANTITE: 15, CLE_SEUIL: 15, CLE_PRIX: 0.15}, False),
    ]
)


def test_verifier_quantite_sous_seuil(produit, booleen_attendu):
    resultat = gestion_stock.verifier_quantite_sous_seuil(produit)

    assert resultat == booleen_attendu


@pytest.mark.parametrize(
    ("produit", "booleen_attendu"),
    [
        ({CLE_NOM: "Banane", CLE_QUANTITE: 3, CLE_SEUIL: 5, CLE_PRIX: 0.35}, False),
        ({CLE_NOM: "Coco", CLE_QUANTITE: 3, CLE_SEUIL: 1, CLE_PRIX: 0.0}, True),
    ]
)


def test_verifier_prix_nul(produit, booleen_attendu):
    resultat = gestion_stock.verifier_prix_nul(produit)

    assert resultat == booleen_attendu