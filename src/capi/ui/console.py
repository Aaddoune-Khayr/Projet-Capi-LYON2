from __future__ import annotations

import sys
from pathlib import Path

from capi.domain.backlog import load_backlog, premiere_fonctionnalite
from capi.domain.moteur_regles import evaluer_vote
from capi.domain.party import Party
from capi.domain.persistence import (
    charger_session,
    exporter_resultats,
    sauvegarder_session,
)
from capi.domain.vote import CARTES_PLANNING_POKER, VoteRound

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKLOG_DEFAUT = REPO_ROOT / "exemples" / "backlog-bibliotheque.json"
SAUVEGARDE_DEFAUT = REPO_ROOT / "sauvegarde.json"
EXPORT_DEFAUT = REPO_ROOT / "resultats.json"


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


def _lire_chemin(prompt: str, default: Path) -> Path:
    raw = _lire_entree(f"{prompt} [{default}] : ")
    path = Path(raw) if raw else default
    if not path.is_absolute() and not path.exists():
        path = REPO_ROOT / path
    return path


def _afficher_cartes() -> None:
    print("Cartes possibles :", ", ".join(CARTES_PLANNING_POKER))


def _lire_regle() -> str:
    while True:
        regle = _lire_entree("Règle de validation (strict/discussion) : ").lower()
        if regle in ("strict", "discussion"):
            return regle
        print("Choisissez « strict » ou « discussion ».")


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


def _annoncer_discussion_extremes(votes: dict[str, str]) -> None:
    rangs = {
        carte: rang
        for rang, carte in enumerate(CARTES_PLANNING_POKER)
        if carte not in ("?", "café")
    }
    votes_utiles = [(pseudo, carte) for pseudo, carte in votes.items() if carte in rangs]
    if not votes_utiles:
        print("Aucun vote exploitable pour désigner les extrêmes.")
        return

    rang_min = min(rangs[carte] for _, carte in votes_utiles)
    rang_max = max(rangs[carte] for _, carte in votes_utiles)
    plus_bas = [pseudo for pseudo, carte in votes_utiles if rangs[carte] == rang_min]
    plus_haut = [pseudo for pseudo, carte in votes_utiles if rangs[carte] == rang_max]
    carte_min = next(carte for _, carte in votes_utiles if rangs[carte] == rang_min)
    carte_max = next(carte for _, carte in votes_utiles if rangs[carte] == rang_max)
    print(
        "Discussion entre les extrêmes : "
        f"{', '.join(plus_bas)} ({carte_min}) et "
        f"{', '.join(plus_haut)} ({carte_max})."
    )


def _lancer_boucle_vote(party: Party, chemin_sauvegarde: Path) -> int | str | None:
    tour = party.tour_courant
    while True:
        print(f"\n=== Tour {tour} ===")
        round_ = _tour_vote_secret(party)
        votes = round_.votes_revelés()
        _reveler_votes(round_)

        if all(carte == "café" for carte in votes.values()):
            party.tour_courant = tour + 1
            sauvegarder_session(party, chemin_sauvegarde)
            print(f"\nPartie sauvegardée dans {chemin_sauvegarde}.")
            return None

        regle = party.regle
        if regle is None:
            raise ValueError("La règle de jeu de la partie n'est pas définie.")
        statut, estimation = evaluer_vote(list(votes.values()), regle, tour)
        if statut == "valide":
            print(f"\nEstimation validée : {estimation}")
            return estimation

        print("\nL'estimation n'est pas validée.")
        if regle == "discussion":
            _annoncer_discussion_extremes(votes)
            _lire_entree("Appuyez sur Entrée après la discussion pour revoter.")
        else:
            print("Un nouveau tour commence.")
        tour += 1


def _choisir_mode() -> str:
    while True:
        print("\n1. Nouvelle partie")
        print("2. Reprendre une partie sauvegardée")
        print("3. Quitter")
        choix = _lire_entree("Votre choix : ")
        if choix in ("1", "2", "3"):
            return choix
        print("Choisissez 1, 2 ou 3.")


def _creer_partie() -> Party:
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
    return party


def _continuer_partie(party: Party, chemin_sauvegarde: Path) -> None:
    if party.regle is None:
        party.regle = _lire_regle()

    while True:
        feature = party.fonctionnalite_courante()
        if feature is None:
            break
        print(f"\nFonctionnalité en cours : [{feature.id}] {feature.titre}")
        estimation = _lancer_boucle_vote(party, chemin_sauvegarde)
        if estimation is None:
            print("Fin de la partie. Vous pourrez la reprendre depuis le menu.")
            return
        party.enregistrer_estimation(estimation)

    export_path = _lire_chemin("Chemin du fichier d'export JSON", EXPORT_DEFAUT)
    exporter_resultats(party, export_path)
    print(f"\nBacklog terminé. Résultats exportés dans {export_path}.")
    print("Fin de la partie.")


def main() -> None:
    print("=== CAPI — Planning poker ===")

    while True:
        mode = _choisir_mode()
        if mode == "3":
            print("\nFin de la partie.")
            return

        if mode == "1":
            party = _creer_partie()
            if _lire_entree(
                "\nLancer un tour de vote pour cette fonctionnalité ? [o/N] : "
            ).lower() not in ("o", "oui", "y", "yes"):
                print("\nFin de la partie.")
                return
            chemin_sauvegarde = SAUVEGARDE_DEFAUT
        else:
            chemin_sauvegarde = _lire_chemin(
                "Chemin de la sauvegarde", SAUVEGARDE_DEFAUT
            )
            try:
                party = charger_session(chemin_sauvegarde)
            except ValueError as exc:
                print(f"Erreur sauvegarde : {exc}")
                continue
            feature = party.fonctionnalite_courante()
            if feature is None:
                print(f"\nPartie chargée : {party.backlog.projet}")
            else:
                print(
                    f"\nPartie chargée : {party.backlog.projet} — "
                    f"reprise à [{feature.id}] {feature.titre}"
                )

        _continuer_partie(party, chemin_sauvegarde)
        return


if __name__ == "__main__":
    main()
