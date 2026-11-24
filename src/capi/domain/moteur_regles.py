from capi.domain.vote import CARTES_PLANNING_POKER

""" J'ai documenté une fonction dans le fichier `moteur_regle.py` (`evaluer_vote`) et deux méthodes dans le fichier `vote.py` (`tous_ont_vote` et `votes_revelés`). Les trois documentations sont donc réparties sur ces deux fichiers. """


def evaluer_vote(votes, regle, tour):
    """
    Permet de savoir si on passe le tour ou si on dois revoter

    Parametres :
        Vote :  la fonction filtre les vote, et regarde si ils sont tous pareille ou pas
        regle :  c'est simplement le fait de verifier si le choix de la regle est bien une des trois regles (strict, mediane, discussion)
        tour : le code regarde si on est au premier tour ou pas, car il y a une regle d'unanimité au premier tour obligatoire

    Returns:
        peut renvoyer plusieurs chose dépandant de la situation :
                - "revote, none" : si il faut revoter
                - "valide, et une estimation" : si le vote est valide

    Raises:
    ValueError : quand il y a une carte invalide ou une règle inconnue
        

    Règle appliquée :
        Si le premier vote est identique au autre, on valide, sinon on revote (apres avoir écarter les carte "?" et "café")
    """

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