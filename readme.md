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
# Lister les agents et leur état
python main.py --list

# Run avec l'objectif par défaut
python main.py

# Run avec un objectif personnalisé
python main.py "Refactorer le composant Settings en TypeScript strict"

# Désactiver certains agents pour ce run
python main.py --skip architect

# Exécuter uniquement certains agents (ordre du YAML conservé)
python main.py --only developer

# Activer des agents désactivés dans le YAML
python main.py --enable developer
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
