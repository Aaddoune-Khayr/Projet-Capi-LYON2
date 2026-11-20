from capi.domain.vote import CARTES_PLANNING_POKER


def evaluer_vote(votes, regle, tour):
    """Évalue l'unanimité; la discussion associée à un revote relève de l'interface."""
    if not votes:
        return "revote", None

    if any(vote not in CARTES_PLANNING_POKER for vote in votes):
        raise ValueError("Un ou plusieurs votes utilisent une carte invalide.")

    votes_utiles = [vote for vote in votes if vote not in ("?", "café")]
    if not votes_utiles:
        return "revote", None

    if tour != 1 and regle not in ("strict", "discussion", "médiane"):
        raise ValueError(f"Règle inconnue : {regle!r}")

    estimation = votes_utiles[0]
    if any(vote != estimation for vote in votes_utiles[1:]):
        return "revote", None

    if estimation == "1/2":
        return "valide", estimation
    return "valide", int(estimation)