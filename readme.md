# agents

Pipeline multi-agents (CrewAI) branché sur un LLM local via LM Studio.
Les agents sont définis **entièrement en YAML** (`config.yaml`) : ajouter un agent = ajouter une entrée, aucun code à modifier.

## Fonctionnement

- Les agents s'exécutent **séquentiellement**, dans l'ordre du YAML.
- Chaque tâche reçoit en contexte la sortie de la tâche précédente.
- `enabled: false` dans le YAML → l'agent est sauté (aucun appel LLM).
- Le LLM pointe vers l'API locale de LM Studio (`http://localhost:1234/v1`), compatible OpenAI.

## Installation

Prérequis : Python 3.10+, [LM Studio](https://lmstudio.ai/) lancé avec un modèle chargé.

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
# Pipeline complet tel que déclaré dans le YAML
python agents/run.py "Ajouter un hook useDebounce dans src/hooks"

# Sauter l'architecte pour une petite tâche bien définie
python agents/run.py "Corrige le bug de useAuth" --skip architect

# Run minimal et rapide : juste le développeur
python agents/run.py "Écris le composant Badge" --only developer

# Activer un agent désactivé dans le YAML pour ce run précis
python agents/run.py "Ajouter le hook + ses tests" --enable tester

# Voir l'état du registre
python agents/run.py --list
#   architect    ✅ actif    — Architecte React Native
#   developer    ✅ actif    — Développeur TypeScript
#   reviewer     ✅ actif    — Relecteur de code
#   tester       ✅ actif    — Ingénieur tests Jest
#   doc          ✅ actif    — Rédacteur technique
```

Le résultat final est écrit dans `output.md`.

## Ajouter un agent

Ajoutez une entrée dans `config.yaml` :

```yaml
- id: reviewer
  enabled: true
  role: "Reviewer TypeScript"
  goal: "Vérifier le code produit avant livraison"
  backstory: >
    Reviewer exigeant, focus typage strict et edge cases.
  tools: [read_file, read_dir]
  task: |
    Objectif du ticket : {objective}

    {context_note}Relis le code produit et signale les problèmes.
  expected_output: "Une liste de corrections avec extraits de code."
```

## Structure

```
agents/
├── config.yaml        # Configuration LLM + définition des agents
├── crew.py            # Construction du crew à partir du YAML
├── main.py            # CLI
├── requirements.txt
└── .gitignore
```
