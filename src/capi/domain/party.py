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
    regle: str | None = None
    estimations: list[int | str] = field(default_factory=list)
    tour_courant: int = 1

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

    def enregistrer_estimation(self, estimation: int | str) -> None:
        if self.fonctionnalite_courante() is None:
            raise ValueError("Aucune fonctionnalité n'est en cours d'estimation.")
        if self.feature_index != len(self.estimations):
            raise ValueError("L'état des estimations de la partie est incohérent.")
        self.estimations.append(estimation)
        self.feature_index += 1
        self.tour_courant = 1
