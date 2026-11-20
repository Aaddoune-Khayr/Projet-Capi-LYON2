# AI_LOG.md : journal d'usage de l'IA

> À placer à la racine du dépôt. À remplir **au fil de l'eau**, pas en fin de projet. Une entrée par tâche (pas par message), en 5 lignes.
> Rappel : l'IA est autorisée pour le **code de production** et la **configuration d'outils** uniquement. Qui a fait la demande, les fichiers touchés et les commits se retrouvent dans l'historique Git : ne les recopiez pas.

## Outils utilisés (à remplir une fois)

| Outil | Modèle (si connu) | Mode (autocomplétion, chat, agent) |
|---|---|---|
| Cursor | Composer | Agent (chat) |

Fichier d'instructions pour agent versionné (`CLAUDE.md`, `AGENTS.md`...) : non

## Entrées

### 2026-10-26 : Walking skeleton Bloc C (US-01, US-02, vote secret)

- **Demande (résumé fidèle)** : Implémenter le skeleton séance 1 : saisie joueurs, chargement backlog JSON, affichage F1, vote caché puis révélation ; séparer domaine et UI ; exemples/ et README ; découpage Git en PR par US.
- **Résultat** : accepté tel quel (relecture copilote avant merge des PR)
- **Ce que nous avons vérifié** : `pip install -e .`, `python -m capi` ; tests domain en Python ; smoke test pipe PowerShell.
- **Ce que nous avons changé ou rejeté, et pourquoi** : pas de validation ni tests auto (séance 2). Vote secret par saisie tour à tour en console.

## Bilan (à compléter en séance 4, 3 lignes)

- Nombre d'entrées et de propositions rejetées ou corrigées :
- Tâches où l'IA a fait gagner du temps :
- Tâches où l'IA a fait perdre du temps :



## Utilisation de l'IA – Bloc B (Configuration CI)

**Outil utilisé :** GitHub Copilot

**Utilisation :** Aide à la création et à la configuration du workflow GitHub Actions (`.github/workflows/ci.yml`).

**Intervention :** Copilot a aidé à définir les déclencheurs du workflow, l'environnement Python, l'installation des dépendances et l'exécution automatique des tests avec pytest.


### Bloc C — Implémentation et intégration du moteur de règles

- **Demande :** Utiliser l'IA pour implémenter le moteur de règles du Planning Poker et l'intégrer dans la boucle de vote de l'application.
- **Résultat :** Proposition acceptée après vérification.
- **Vérifications :** Exécution de `python -m pytest` : 6 tests réussis. Vérification des parcours console avec les règles `strict` et `discussion`. Exécution de `git diff --check` sans erreur.
- **Modifications :** Implémentation de `evaluer_vote`, intégration dans `console.py` et mise à jour du `README.md`. Aucun test n'a été modifié.