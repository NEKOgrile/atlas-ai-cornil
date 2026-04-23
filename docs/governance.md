# Gouvernance

Cette page explique les règles de sécurité et les guardrails implémentés dans ATLAS.

## Objectif

- Empêcher les requêtes interdites
- Masquer les informations sensibles
- Protéger le modèle contre les injections de prompt
- Contrôler le volume de requêtes

## Guardrails implémentés

Le module `atlas/guardrails.py` applique plusieurs règles :

1. Détection de PII simple
   - masque les numéros de carte bancaire de 16 chiffres en `"[CB_MASKED]"`
2. Blocage de sujets interdits
   - sujets listés dans `config/atlas.yaml > guardrails.blocked_topics`
3. Limitation de longueur
   - message trop long bloque la requête
4. Détection de prompt injection
   - motifs comme `ignore previous`, `tu es maintenant`, `<|system|>`
5. Rate limiting local
   - limite le nombre de requêtes par minute

## Comportement

- Si une règle est déclenchée, le message est repris ou refusé.
- L'utilisateur reçoit un retour clair (`rules: [...]`).
- Les requêtes bloquées ne sont pas envoyées à Ollama.

## RGPD et confidentialité

- Les messages sont tronqués dans les logs (`atlas/monitoring.py`).
- La trace conserve seulement les 200 premiers caractères de l'entrée et de la sortie.
- Le suivi est conçu pour être auditable sans stocker de longs textes clients.

## Désactivation

Pour désactiver les guardrails, lancer :

```bash
python atlas_chat.py chat --no-guardrails
```

## Tests unitaires

Les règles sont testées dans `tests/test_guardrails.py`.
Ces tests vérifient le masquage PII, le blocage de sujets et la détection de prompt injection.
