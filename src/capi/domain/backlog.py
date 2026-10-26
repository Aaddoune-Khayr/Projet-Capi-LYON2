from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Feature:
    id: str
    titre: str


@dataclass(frozen=True)
class Backlog:
    projet: str
    fonctionnalites: tuple[Feature, ...]


def load_backlog(path: Path | str) -> Backlog:
    """Charge un backlog JSON. Lève ValueError si le fichier ou le schéma est invalide."""
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Fichier backlog introuvable : {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON invalide : {path}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Le backlog doit être un objet JSON.")

    projet = raw.get("projet")
    if not isinstance(projet, str) or not projet.strip():
        raise ValueError('Champ "projet" manquant ou invalide.')

    items = raw.get("fonctionnalites")
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError('Champ "fonctionnalites" doit être une liste non vide.')

    features: list[Feature] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"fonctionnalites[{index}] doit être un objet.")
        fid = item.get("id")
        titre = item.get("titre")
        if not isinstance(fid, str) or not fid.strip():
            raise ValueError(f"fonctionnalites[{index}].id invalide.")
        if not isinstance(titre, str) or not titre.strip():
            raise ValueError(f"fonctionnalites[{index}].titre invalide.")
        features.append(Feature(id=fid.strip(), titre=titre.strip()))

    return Backlog(projet=projet.strip(), fonctionnalites=tuple(features))


def premiere_fonctionnalite(backlog: Backlog) -> Feature | None:
    if not backlog.fonctionnalites:
        return None
    return backlog.fonctionnalites[0]
