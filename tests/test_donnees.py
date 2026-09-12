import pytest

import donnees


@pytest.mark.parametrize(
    ("objet_teste", "resultat_attendu"),
    [
        (
            [1, 2, 3],
            donnees.ResultatChargementFichier.SUCCES),
        (
            {"nom": "coco", "quantite": 2},
            donnees.ResultatChargementFichier.STOCK_PAS_UNE_LISTE
         ),
    ]
)


def test__verifier_structure_stock(objet_teste, resultat_attendu):
    resultat = donnees._verifier_structure_stock(objet_teste)

    assert resultat == resultat_attendu