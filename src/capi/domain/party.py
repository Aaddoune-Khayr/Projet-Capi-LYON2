from __future__ import annotations

from dataclasses import dataclass, field

from capi.domain.backlog import Backlog


@dataclass(frozen=True)
class Player:
    pseudo: str


@dataclass
class Party:
    """État d'une partie (sans règles de validation — séance 2)."""

    players: tuple[Player, ...]
    backlog: Backlog | None = None
    feature_index: int = 0

    @staticmethod
    def creer_joueurs(pseudos: list[str]) -> tuple[Player, ...]:
        cleaned = [p.strip() for p in pseudos if p.strip()]
        if len(cleaned) != len(pseudos):
            raise ValueError("Tous les pseudos doivent être non vides.")
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("Les pseudos doivent être distincts.")
        return tuple(Player(pseudo=p) for p in cleaned)

    def attacher_backlog(self, backlog: Backlog) -> None:
        self.backlog = backlog
        self.feature_index = 0

    def fonctionnalite_courante(self):
        if self.backlog is None:
            return None
        if self.feature_index >= len(self.backlog.fonctionnalites):
            return None
        return self.backlog.fonctionnalites[self.feature_index]
