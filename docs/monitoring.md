# Monitoring

ATLAS enregistre chaque interaction dans `logs/traces.jsonl`.
Cette trace sert à l'analyse de performance et à l'audit.

## Format des traces

Chaque ligne JSON contient :

- `timestamp` : date et heure ISO
- `session_id` : identifiant de session
- `model` : modèle utilisé
- `user_message` : message utilisateur tronqué
- `assistant_message` : réponse du modèle tronquée
- `prompt_tokens` : tokens estimés en entrée
- `completion_tokens` : tokens estimés en sortie
- `latency_ms` : latence de l'appel en millisecondes
- `memory_hits` : nombre de souvenirs injectés
- `metadata` : informations additionnelles

## Comment c'est implémenté

- `atlas/monitoring.py` contient `TraceLogger`.
- `atlas/cli.py` appelle `logger.log_interaction()` à chaque réponse du modèle.
- Les messages clients sont tronqués pour limiter la surface RGPD.

## Analyse des traces

Le script `scripts/analyze_traces.py` calcule :

- nombre d'interactions
- latence moyenne
- latence médiane
- latence p95
- distribution des tokens
- estimations de coût GPT-4o

### Exécution

```bash
python scripts/analyze_traces.py
```

### Résultats

Le script affiche également les requêtes les plus lentes et produit un histogramme des tokens.

## Bonnes pratiques

- Garder `logs/traces.jsonl` sous contrôle de version uniquement si les données sont anonymisées.
- Purger régulièrement les anciennes traces si le fichier devient volumineux.
- Ne pas stocker de PII sensibles dans les traces brutes.
