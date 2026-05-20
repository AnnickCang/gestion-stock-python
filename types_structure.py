from typing import TypedDict


class Produit(TypedDict):
    nom: str
    quantite: int
    seuil: int
    prix: float


class ChampsNumeriquesProduit(TypedDict):
    quantite: int
    seuil: int
    prix: float