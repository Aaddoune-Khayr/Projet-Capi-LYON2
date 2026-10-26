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
