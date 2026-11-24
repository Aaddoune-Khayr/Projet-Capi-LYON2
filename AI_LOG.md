# AI_LOG.md : journal d'usage de l'IA

> À placer à la racine du dépôt. À remplir **au fil de l'eau**, pas en fin de projet. Une entrée par tâche (pas par message), en 5 lignes.
> Rappel : l'IA est autorisée pour le **code de production** et la **configuration d'outils** uniquement. Qui a fait la demande, les fichiers touchés et les commits se retrouvent dans l'historique Git : ne les recopiez pas.

## Outils utilisés (à remplir une fois)

| Outil | Modèle (si connu) | Mode (autocomplétion, chat, agent) |
|---|---|---|
| Cursor | Composer | Agent (chat) |
| Copilot | Copilot fusion | Agent (chat) |

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

### 2026-11-24 : Génération automatique de la documentation Python (Bloc C2)

- **Demande :** Ajouter à la CI GitHub Actions la génération de documentation du package Python `capi` (situé dans `src/capi`), puis conserver le résultat comme artefact du workflow.
- **Intervention de l'IA :** Configuration dans `.github/workflows/ci.yml` de l'installation de pdoc, de la commande `python -m pdoc capi -o site` et de la sauvegarde du dossier `site` avec `actions/upload-artifact@v4` sous le nom `documentation`.
- **Vérification :** Exécution locale de `python -m pdoc capi -o site` réussie ; six fichiers HTML ont été générés.
- **Modifications :** Ajout de `site/` à `.gitignore` afin que le résultat généré ne soit pas ajouté au dépôt. Aucune fonction métier, aucun test ni aucune docstring n'a été modifié.

### 2026-11-24 : Persistance et export du Bloc D

- **Demande :** Vérifier puis compléter l'export final JSON, la sauvegarde sur vote unanime « café », la reprise de partie et la cohérence du chargement.
- **Modifications :** Ajout de la sauvegarde et du chargement de l'état de partie, du tour de vote à reprendre et de l'export final dans `src/capi/domain/persistence.py`, du suivi des estimations dans `party.py`, du traitement de toutes les fonctionnalités, du menu de reprise et de la sauvegarde café dans `console.py`. Le chargement du backlog réutilise maintenant la validation de ses données JSON dans `backlog.py`.
- **Vérifications :** `python -m pytest` (6 tests réussis), `python -m compileall -q src` et `git diff --check` réussis. Une simulation temporaire a vérifié l'égalité exacte après sauvegarde/chargement, la sauvegarde sur unanimité « café », la reprise de la fonctionnalité et du numéro de tour, ainsi que l'export complet avec les estimations et la règle. Aucun fichier de test, aucune fonction de test, aucune docstring et aucun commentaire n'a été ajouté ou modifié.

### 2026-11-25 : Versionnement et écriture atomique des sauvegardes

- **Corrections :** Versionnement des sauvegardes (version 2) et migration des fichiers non versionnés comme version 1, avec valeurs déduites ou par défaut pour les champs récents absents ; remplacement de l'écriture directe par un fichier temporaire suivi d'un remplacement atomique et d'un nettoyage en cas d'échec.
- **Vérifications :** `python -m pytest` (6 tests réussis), `python -m compileall -q src` et `git diff --check` réussis. Vérifications temporaires de l'aller-retour versionné, de la migration d'une ancienne sauvegarde sans `tour_courant`, de la conservation de la sauvegarde existante et du nettoyage du temporaire après échec du remplacement. Aucun test, docstring ou commentaire n'a été modifié.
