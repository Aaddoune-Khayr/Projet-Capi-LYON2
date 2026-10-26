from __future__ import annotations

import sys
from pathlib import Path

from capi.domain.backlog import load_backlog, premiere_fonctionnalite
from capi.domain.party import Party
from capi.domain.vote import CARTES_PLANNING_POKER, VoteRound

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKLOG_DEFAUT = REPO_ROOT / "exemples" / "backlog-bibliotheque.json"


def _lire_entree(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        print()
        sys.exit(0)


def _lire_nombre_joueurs() -> int:
    while True:
        raw = _lire_entree("Nombre de joueurs : ")
        try:
            n = int(raw)
            if n < 1:
                raise ValueError
            return n
        except ValueError:
            print("Entrez un entier ≥ 1.")


def _lire_pseudos(n: int) -> list[str]:
    pseudos: list[str] = []
    for i in range(1, n + 1):
        while True:
            pseudo = _lire_entree(f"Pseudo du joueur {i}/{n} : ")
            if not pseudo:
                print("Le pseudo ne peut pas être vide.")
                continue
            if pseudo in pseudos:
                print("Ce pseudo est déjà pris.")
                continue
            pseudos.append(pseudo)
            break
    return pseudos


def _lire_chemin_backlog() -> Path:
    suggestion = str(BACKLOG_DEFAUT)
    raw = _lire_entree(f"Chemin du backlog JSON [{suggestion}] : ")
    path = Path(raw) if raw else BACKLOG_DEFAUT
    if not path.is_file():
        path = REPO_ROOT / path
    return path


def _afficher_cartes() -> None:
    print("Cartes possibles :", ", ".join(CARTES_PLANNING_POKER))


def _tour_vote_secret(party: Party) -> VoteRound:
    round_ = VoteRound()
    pseudos = tuple(p.pseudo for p in party.players)
    print("\n--- Tour de vote (secret) ---")
    _afficher_cartes()
    for player in party.players:
        print(f"\n>>> {player.pseudo} : à vous de voter.")
        print("    (Les autres joueurs ne doivent pas regarder l'écran.)")
        while True:
            carte = _lire_entree("Votre carte : ")
            try:
                round_.enregistrer_vote(player.pseudo, carte)
                break
            except ValueError as exc:
                print(exc)
    assert round_.tous_ont_vote(pseudos)
    return round_


def _reveler_votes(round_: VoteRound) -> None:
    print("\n--- Révélation des votes ---")
    for pseudo, carte in round_.votes_revelés().items():
        print(f"  {pseudo} : {carte}")
    print("(La validation des votes sera ajoutée en séance 2.)")


def main() -> None:
    print("=== CAPI — Planning poker (walking skeleton) ===\n")

    n = _lire_nombre_joueurs()
    try:
        players = Party.creer_joueurs(_lire_pseudos(n))
    except ValueError as exc:
        print(exc)
        sys.exit(1)

    party = Party(players=players)

    path = _lire_chemin_backlog()
    try:
        backlog = load_backlog(path)
    except ValueError as exc:
        print(f"Erreur backlog : {exc}")
        sys.exit(1)

    party.attacher_backlog(backlog)
    feature = premiere_fonctionnalite(backlog)
    if feature is None:
        print("Le backlog ne contient aucune fonctionnalité.")
        sys.exit(1)

    print(f"\nProjet : {backlog.projet}")
    print(f"Fonctionnalité en cours : [{feature.id}] {feature.titre}")

    if _lire_entree("\nLancer un tour de vote pour cette fonctionnalité ? [o/N] : ").lower() in (
        "o",
        "oui",
        "y",
        "yes",
    ):
        round_ = _tour_vote_secret(party)
        _reveler_votes(round_)

    print("\nFin du skeleton pour cette séance. À bientôt pour la séance 2.")


if __name__ == "__main__":
    main()
