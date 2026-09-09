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