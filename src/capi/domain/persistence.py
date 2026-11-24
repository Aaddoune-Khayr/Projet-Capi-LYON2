from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from capi.domain.backlog import backlog_from_data
from capi.domain.party import Party
from capi.domain.vote import CARTES_PLANNING_POKER

_REGLES_VALIDES = ("strict", "discussion")
_ESTIMATIONS_VALIDES = frozenset(
    carte for carte in CARTES_PLANNING_POKER if carte not in ("?", "café")
)
_VERSION_FORMAT = 2


def sauvegarder_session(party: Party, path: Path | str) -> None:
    backlog = party.backlog
    if backlog is None:
        raise ValueError("Impossible de sauvegarder une partie sans backlog.")
    if party.regle not in _REGLES_VALIDES:
        raise ValueError("La règle de jeu de la partie est absente ou invalide.")
    if party.feature_index != len(party.estimations):
        raise ValueError("L'état des estimations de la partie est incohérent.")
    if party.feature_index > len(backlog.fonctionnalites):
        raise ValueError("L'index de fonctionnalité de la partie est invalide.")
    if (
        isinstance(party.tour_courant, bool)
        or not isinstance(party.tour_courant, int)
        or party.tour_courant < 1
    ):
        raise ValueError("Le numéro de tour de la partie est invalide.")

    current = party.fonctionnalite_courante()
    data = {
        "version": _VERSION_FORMAT,
        "joueurs": [player.pseudo for player in party.players],
        "regle": party.regle,
        "backlog": {
            "projet": backlog.projet,
            "fonctionnalites": [
                {"id": feature.id, "titre": feature.titre}
                for feature in backlog.fonctionnalites
            ],
        },
        "fonctionnalites_estimees": [
            {
                "id": feature.id,
                "titre": feature.titre,
                "difficulte_estimee": estimation,
            }
            for feature, estimation in zip(
                backlog.fonctionnalites, party.estimations
            )
        ],
        "index_fonctionnalite_courante": party.feature_index,
        "tour_courant": party.tour_courant,
        "fonctionnalite_en_cours": (
            {"id": current.id, "titre": current.titre}
            if current is not None
            else None
        ),
    }
    _ecrire_json(data, path)


def charger_session(path: Path | str) -> Party:
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Fichier de sauvegarde introuvable : {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Fichier de sauvegarde JSON invalide : {path}") from exc
    except OSError as exc:
        raise ValueError(f"Impossible de lire la sauvegarde : {path}") from exc

    if not isinstance(data, dict):
        raise ValueError("La sauvegarde doit être un objet JSON.")

    version = data.get("version", 1)
    if (
        isinstance(version, bool)
        or not isinstance(version, int)
        or version not in (1, 2)
    ):
        raise ValueError(f"Version de sauvegarde non prise en charge : {version!r}")

    joueurs = data.get("joueurs")
    if (
        not isinstance(joueurs, list)
        or not joueurs
        or any(not isinstance(pseudo, str) for pseudo in joueurs)
    ):
        raise ValueError("La liste des joueurs de la sauvegarde est invalide.")
    players = Party.creer_joueurs(joueurs)

    regle = data.get("regle")
    if regle not in _REGLES_VALIDES:
        raise ValueError("La règle de jeu de la sauvegarde est invalide.")

    backlog = backlog_from_data(data.get("backlog"))
    raw_estimations = data.get("fonctionnalites_estimees")
    if not isinstance(raw_estimations, list):
        raise ValueError("La liste des fonctionnalités estimées est invalide.")

    if "index_fonctionnalite_courante" not in data and version == 1:
        index = len(raw_estimations)
    else:
        index = data.get("index_fonctionnalite_courante")
    if (
        isinstance(index, bool)
        or not isinstance(index, int)
        or index < 0
        or index > len(backlog.fonctionnalites)
    ):
        raise ValueError("L'index de fonctionnalité de la sauvegarde est invalide.")

    if "tour_courant" not in data and version == 1:
        tour = 1
    else:
        tour = data.get("tour_courant")
    if (
        isinstance(tour, bool)
        or not isinstance(tour, int)
        or tour < 1
    ):
        raise ValueError("Le numéro de tour de la sauvegarde est invalide.")

    if len(raw_estimations) != index:
        raise ValueError("La liste des fonctionnalités estimées est invalide.")

    estimations: list[int | str] = []
    for feature, saved in zip(backlog.fonctionnalites, raw_estimations):
        if (
            not isinstance(saved, dict)
            or saved.get("id") != feature.id
            or saved.get("titre") != feature.titre
        ):
            raise ValueError("Une fonctionnalité estimée ne correspond pas au backlog.")
        estimation = saved.get("difficulte_estimee")
        if (
            isinstance(estimation, bool)
            or not isinstance(estimation, (int, str))
            or str(estimation) not in _ESTIMATIONS_VALIDES
        ):
            raise ValueError("Une difficulté estimée dans la sauvegarde est invalide.")
        estimations.append(estimation)

    if "fonctionnalite_en_cours" not in data and version != 1:
        raise ValueError("La fonctionnalité en cours est absente de la sauvegarde.")
    current = (
        backlog.fonctionnalites[index]
        if index < len(backlog.fonctionnalites)
        else None
    )
    expected_current = (
        {"id": current.id, "titre": current.titre}
        if current is not None
        else None
    )
    if (
        "fonctionnalite_en_cours" in data
        and data["fonctionnalite_en_cours"] != expected_current
    ):
        raise ValueError("La fonctionnalité en cours ne correspond pas au backlog.")

    return Party(
        players=players,
        backlog=backlog,
        feature_index=index,
        regle=regle,
        estimations=estimations,
        tour_courant=tour,
    )


def exporter_resultats(party: Party, path: Path | str) -> None:
    backlog = party.backlog
    if backlog is None:
        raise ValueError("Impossible d'exporter une partie sans backlog.")
    if party.regle not in _REGLES_VALIDES:
        raise ValueError("La règle de jeu de la partie est absente ou invalide.")
    if (
        party.feature_index != len(backlog.fonctionnalites)
        or len(party.estimations) != len(backlog.fonctionnalites)
    ):
        raise ValueError("Le backlog doit être entièrement estimé avant l'export.")

    data = {
        "projet": backlog.projet,
        "regle": party.regle,
        "fonctionnalites": [
            {
                "id": feature.id,
                "titre": feature.titre,
                "difficulte_estimee": estimation,
            }
            for feature, estimation in zip(
                backlog.fonctionnalites, party.estimations
            )
        ],
    }
    _ecrire_json(data, path)


def _ecrire_json(data: dict, path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
