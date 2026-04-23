# Sécurité

Ce document décrit le modèle de menace et les décisions de sécurité prises pour ATLAS.

## Contexte

ATLAS doit rester 100% on-premise et ne pas envoyer de données clients à des services cloud externes.

## Principes de sécurité

- Pas d'appel API externe pour le modèle.
- Stockage local des traces et de la mémoire.
- Masquage des informations sensibles avant envoi au modèle.
- Validation des entrées pour limiter les abus.

## Menaces couvertes

### 1. Fuite de données

- Aucun appel à OpenAI, Anthropic ou autre API cloud.
- Les données restent sur la machine de l'utilisateur.

### 2. PII dans les prompts

- Le module `atlas/guardrails.py` détecte et masque les numéros de carte bancaire de 16 chiffres.
- Le nettoyage est appliqué avant l'appel à Ollama.

### 3. Prompt injection

- Le système bloque les requêtes contenant des motifs suspects comme `ignore previous`, `tu es maintenant` ou `<|system|>`.

### 4. Déni de service local

- Le rate limiting empêche un même utilisateur d'envoyer trop de requêtes par minute.

## Journaux et RGPD

- `logs/traces.jsonl` contient des messages tronqués pour limiter l'exposition.
- Les attributs `user_message` et `assistant_message` sont limités à 200 caractères.

## Décisions de conception

- La configuration est externe (`config/atlas.yaml`) pour éviter de recompiler le modèle à chaque changement.
- Le `Modelfile` existe pour ceux qui veulent un modèle Ollama custom, mais la CLI est conçue pour utiliser la configuration en code.
- Le projet privilégie la transparence et la traçabilité plutôt que les optimisations complexes.
