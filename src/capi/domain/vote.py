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
        """
        Verifie que tout les joueur ont voté

        Parametres : Pseudos : ceci est la liste des joueurs qui doivent voter

        Returns: true si tout les joueurs ont voté, sinon False
            
        Règle appliquée : regarde si tout les pseudo attendu du dictionnaire sont dans le vote (afin de verifié si il manque pas un joueur qui n'a pas encore voté)

        """
        return set(pseudos) <= set(self.votes.keys())




    def votes_revelés(self) -> dict[str, str]:
        """
         cette fonction recuperer les votes (elle copie le dictionnaire de vote et le renvoie)

        Parametres : ne prend pas de parametre en dehors de "self"

        Returns: cette fonction renvoi le dictionnaire des votes, avec le pseudo, et le vote (copie du dictionnaire de vote)        
            
        Règle appliquée : renvoie le dictonnaire des votes 
        
        """
        return dict(self.votes)
