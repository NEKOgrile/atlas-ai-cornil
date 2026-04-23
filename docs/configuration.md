# Configuration

Le comportement du projet est défini dans `config/atlas.yaml`.
Il est chargé par `atlas/cli.py` avec un schéma Pydantic dans `atlas/config/schema.py`.

## Structure du fichier

```yaml
model:
  name: "atlas-tuned"
  temperature: 0.3
  top_p: 0.9
  num_ctx: 4096
  timeout: 300

persona:
  name: "Atlas"
  system_prompt: |
    tu es atlas
    tu réponds court
    pas de blabla

memory:
  enabled: true
  top_k: 5
  min_similarity: 0.7
  max_short_term: 50

guardrails:
  enabled: true
  blocked_topics:
    - "politique"
    - "religion"

logging:
  level: "INFO"
  path: "./logs/traces.jsonl"
```

## Options principales

### `model`

- `name` : modèle Ollama utilisé
- `temperature` : créativité du modèle (0 à 1)
- `top_p` : paramètre nucleus sampling
- `num_ctx` : taille de contexte
- `timeout` : durée limite de requête en secondes

### `persona`

- `name` : nom de l'assistant
- `system_prompt` : instructions système injectées à chaque appel

### `memory`

- `enabled` : active ou désactive la mémoire persistante
- `top_k` : nombre de souvenirs à récupérer
- `min_similarity` : seuil approximatif de similarité pour la recherche
- `max_short_term` : nombre maximum de messages conservés en mémoire courte

### `guardrails`

- `enabled` : active ou désactive les règles de sécurité
- `blocked_topics` : sujets interdits bloqués automatiquement

### `logging`

- `level` : niveau de journalisation
- `path` : emplacement du fichier de traces JSONL

## Validation

La configuration est validée par `AtlasConfig` dans `atlas/config/schema.py`.
Si le YAML est invalide, le CLI affiche un message d'erreur et cesse de démarrer.

## Modification rapide

Pour changer le comportement sans toucher au code :

- modifier `config/atlas.yaml`
- relancer `python atlas_chat.py chat`

Exemple : augmenter la créativité

```yaml
model:
  temperature: 0.7
```
