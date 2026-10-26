from __future__ import annotations

from dataclasses import dataclass, field

CARTES_PLANNING_POKER: tuple[str, ...] = (
    "0",
    "1/2",
    "1",
    "2",
    "3",
    "5",
    "8",
    "13",
    "21",
    "?",
    "café",
)


@dataclass
class VoteRound:
    """Un tour de vote (sans validation ni nouveau tour — séance 2)."""

    votes: dict[str, str] = field(default_factory=dict)

    def enregistrer_vote(self, pseudo: str, carte: str) -> None:
        if carte not in CARTES_PLANNING_POKER:
            raise ValueError(f"Carte invalide : {carte!r}")
        if pseudo in self.votes:
            raise ValueError(f"{pseudo} a déjà voté.")
        self.votes[pseudo] = carte

    def tous_ont_vote(self, pseudos: tuple[str, ...]) -> bool:
        return set(pseudos) <= set(self.votes.keys())

    def votes_revelés(self) -> dict[str, str]:
        return dict(self.votes)
