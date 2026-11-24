from capi.domain.backlog import Backlog, Feature
from capi.domain.party import Party
from capi.domain.persistence import sauvegarder_session, charger_session


def test_sauvegarde_chargement_identique(tmp_path):

    # Préparer
    joueurs = Party.creer_joueurs(["Abdennour", "Lola"])
    backlog = Backlog(
        "Mon projet",
        (
            Feature("1", "Première fonctionnalité"),
            Feature("2", "Deuxième fonctionnalité"),
        )
    )

    partie = Party(
        players=joueurs,
        backlog=backlog,
        feature_index=1,
        regle="strict",
        estimations=[5],
        tour_courant=3  
    )

    chemin = tmp_path / "sauvegarde.json"

    # Agir
    sauvegarder_session(partie, chemin)
    partie_chargee = charger_session(chemin)

    # Vérifier
    assert partie_chargee == partie