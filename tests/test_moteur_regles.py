from capi.domain.moteur_regles import evaluer_vote

def test_CA_02_1_strict_revote1():

    # Préparer
    votes = ["3", "5", "8", "5"]
    regle = "strict"
    tour = 1

    # Agir
    resultat = evaluer_vote(votes, regle, tour)

    # Vérifier
    assert resultat == ("revote", None)


def test_CA_03_2_strict_Valide1():

    # Préparer
    votes = ["5", "5", "5", "5"]
    regle = "strict"
    tour = 1

    # Agir
    resultat = evaluer_vote(votes, regle, tour)

    # Vérifier
    assert resultat == ("valide", None)


def test_CA_xx_y_strict_revote2():

    # Préparer
    votes = ["5", "5", "5", "3"]
    regle = "strict"
    tour = 2

    # Agir
    resultat = evaluer_vote(votes, regle, tour)

    # Vérifier
    assert resultat == ("revote", None)



def test_CA_xx_y_mediane_revote3():

    # Préparer
    votes = ["5", "5", "3", "?"]
    regle = "médiane"
    tour = 2

    # Agir
    resultat = evaluer_vote(votes, regle, tour)

    # Vérifier
    assert resultat == ("revote", None)




def test_CA_xx_y_mediane_Valide2():

    # Préparer
    votes = ["5", "5", "5", "?"]
    regle = "médiane"
    tour = 2

    # Agir
    resultat = evaluer_vote(votes, regle, tour)

    # Vérifier
    assert resultat == ("valide", None)





def test_CA_xx_y_strict_Valide3():

    # Préparer
    votes = ["5", "5", "5", "?"]
    regle = "strict"
    tour = 2

    # Agir
    resultat = evaluer_vote(votes, regle, tour)

    # Vérifier
    assert resultat == ("valide", None)