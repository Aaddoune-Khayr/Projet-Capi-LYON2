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

## Organisation du code

| Dossier | Rôle |
|---|---|
| `src/capi/domain/` | Logique métier (partie, backlog, votes) |
| `src/capi/ui/` | Interface console |

**Choix techniques (brouillon ADR-01)** : Python pour la simplicité du walking skeleton, la lecture JSON native et les tests unitaires prévus en séance 2. La séparation `domain` / `ui` permet de tester les règles de validation sans lancer la console.
