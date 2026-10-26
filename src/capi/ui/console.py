from __future__ import annotations

import sys

from capi.domain.party import Party


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


def main() -> None:
    print("=== CAPI — Planning poker (walking skeleton) ===\n")

    n = _lire_nombre_joueurs()
    try:
        players = Party.creer_joueurs(_lire_pseudos(n))
    except ValueError as exc:
        print(exc)
        sys.exit(1)

    party = Party(players=players)
    print(f"\nPartie configurée avec {len(party.players)} joueur(s) :")
    for player in party.players:
        print(f"  - {player.pseudo}")


if __name__ == "__main__":
    main()
