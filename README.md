# CAPI — Planning poker

Binôme **B12** (Abdennour et Lola). Application d'estimation de backlog par planning poker.

## Prérequis

- Python **3.10** ou plus récent
- Git

## Lancer l'application (après clone)

```bash
git clone https://github.com/Aaddoune-Khayr/Projet-Capi-LYON2.git
cd "Projet CAPI"
pip install -e .
python -m capi
```

## Format du backlog JSON

Fichier d'exemple : `exemples/backlog-bibliotheque.json`.

| Champ | Type | Description |
|---|---|---|
| `projet` | string | Nom du projet estimé |
| `fonctionnalites` | array | Liste ordonnée des US / fonctionnalités à estimer |
| `fonctionnalites[].id` | string | Identifiant stable (ex. `F1`) |
| `fonctionnalites[].titre` | string | Intitulé affiché aux joueurs |

Au lancement, l'application affiche la **première** entrée de `fonctionnalites`.

## Tests

Les tests automatisés arrivent en **séance 2**. Pour l'instant, vérifiez à la main en lançant `python -m capi`.

## Organisation du code

| Dossier | Rôle |
|---|---|
| `src/capi/domain/` | Logique métier (partie, backlog, votes) |
| `src/capi/ui/` | Interface console |
| `exemples/` | Données JSON d'exemple |

**Choix techniques (brouillon ADR-01)** : Python pour la simplicité du walking skeleton, la lecture JSON native et les tests unitaires prévus en séance 2. La séparation `domain` / `ui` permet de tester les règles de validation sans lancer la console.

## GitHub Flow (variante cours)

- Une branche par US (`us-02-chargement-backlog`, etc.)
- Commits préfixés : `feat(US-02): ...`
- Une PR par US, relue par le copilote avant fusion
