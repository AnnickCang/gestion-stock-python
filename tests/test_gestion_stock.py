import pytest

import gestion_stock
import types_structure


@pytest.mark.parametrize(
    ("nom_recherche", "produit_attendu"),
    [
        ("banane", None),
        ("café", {"nom": "Café", "quantite": 3, "seuil": 2, "prix": 18.5}),
        ("cafe", {"nom": "Café", "quantite": 3, "seuil": 2, "prix": 18.5}),
    ],
)


def test_trouver_produit(nom_recherche, produit_attendu):
    stock: list[types_structure.Produit] = [
        {"nom": "bonbon", "quantite": 15, "seuil": 5, "prix": 0.5},
        {"nom": "Café", "quantite": 3, "seuil": 2, "prix": 18.5},
        {"nom": "CHOCOLAT", "quantite": 1, "seuil": 2, "prix": 3.75},
        {"nom": "M&M's", "quantite": 10, "seuil": 3, "prix": 2.5},
        {"nom": "Tomate cerise", "quantite": 5, "seuil": 10, "prix": 0.75},
    ]

    resultat = gestion_stock.trouver_produit(stock, nom_recherche)

    assert resultat == produit_attendu


def test_ajouter_produit():
    stock: list[types_structure.Produit] = [
        {"nom": "bonbon", "quantite": 15, "seuil": 5, "prix": 0.5},
        {"nom": "Café", "quantite": 3, "seuil": 2, "prix": 18.5},
    ]
    stock_attendu: list[types_structure.Produit] = [
        {"nom": "bonbon", "quantite": 15, "seuil": 5, "prix": 0.5},
        {"nom": "Café", "quantite": 3, "seuil": 2, "prix": 18.5},
        {"nom": "CHOCOLAT", "quantite": 1, "seuil": 2, "prix": 3.75},
    ]
    nom = "CHOCOLAT"
    quantite = 1
    seuil = 2
    prix = 3.749

    gestion_stock.ajouter_produit(stock, nom, quantite, seuil, prix)

    assert stock == stock_attendu


def test_modifier_produit():
    produit_a_modifier: types_structure.Produit = {
        "nom": "CHOCOLAT",
        "quantite": 1,
        "seuil": 2,
        "prix": 3.75
    }
    nouvelle_quantite = 5
    nouveau_seuil = 3
    nouveau_prix = 2.233
    produit_attendu: types_structure.Produit = {
        "nom": "CHOCOLAT",
        "quantite": 5,
        "seuil": 3,
        "prix": 2.23
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
        {"nom": "bonbon", "quantite": 5, "seuil": 5, "prix": 0.5},
        {"nom": "Café", "quantite": 1, "seuil": 2, "prix": 18.5},
        {"nom": "CHOCOLAT", "quantite": 3, "seuil": 2, "prix": 3.75},
        {"nom": "M&M's", "quantite": 10, "seuil": 3, "prix": 2.5},
        {"nom": "noix de Cajou", "quantite": 10, "seuil": 10, "prix": 0.75},
        {"nom": "Tomate cerise", "quantite": 5, "seuil": 10, "prix": 0.75},
    ]
    alertes_attendues: list[types_structure.Produit] = [
        {"nom": "Café", "quantite": 1, "seuil": 2, "prix": 18.5},
        {"nom": "Tomate cerise", "quantite": 5, "seuil": 10, "prix": 0.75},
    ]

    resultat = gestion_stock.trouver_alertes(stock)

    assert resultat == alertes_attendues


def test_supprimer_produit():
    stock: list[types_structure.Produit] = [
        {"nom": "bonbon", "quantite": 5, "seuil": 5, "prix": 0.5},
        {"nom": "Café", "quantite": 1, "seuil": 2, "prix": 18.5},
        {"nom": "CHOCOLAT", "quantite": 3, "seuil": 2, "prix": 3.75},
    ]
    produit_a_supprimer: types_structure.Produit = {
        "nom": "Café",
        "quantite": 1,
        "seuil": 2,
        "prix": 18.5
    }
    stock_attendu: list[types_structure.Produit] = [
        {"nom": "bonbon", "quantite": 5, "seuil": 5, "prix": 0.5},
        {"nom": "CHOCOLAT", "quantite": 3, "seuil": 2, "prix": 3.75},
    ]

    gestion_stock.supprimer_produit(stock, produit_a_supprimer)

    assert stock == stock_attendu


def test_renommer_produit():
    produit: types_structure.Produit = {
        "nom": "Café",
        "quantite": 1,
        "seuil": 2,
        "prix": 18.5
    }
    nouveau_nom = "Décaféiné"
    produit_attendu: types_structure.Produit = {
            "nom": "Décaféiné",
            "quantite": 1,
            "seuil": 2,
            "prix": 18.5
        }

    gestion_stock.renommer_produit(produit, nouveau_nom)

    assert produit == produit_attendu