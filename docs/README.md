# Documentation ATLAS

Ce dossier contient la documentation projet pour qu'un autre développeur ou un client puisse reprendre le travail sans assistance.

## Objectif

- Expliquer le fonctionnement du projet
- Montrer comment installer et démarrer
- Documenter la configuration, le monitoring, les guardrails et l'exploitation
- Fournir des décisions d'architecture claires

## Contenu

- `docs/installation.md` : installation, dépendances et démarrage
- `docs/configuration.md` : structure du YAML et options disponibles
- `docs/architecture.md` : architecture logicielle et décisions
- `docs/monitoring.md` : logs, traces et analyse des métriques
- `docs/governance.md` : guardrails, RGPD et règles de sécurité
- `docs/operations.md` : runbook opérationnel
- `docs/security.md` : modèle de menace et choix de sécurité
- `docs/ADR-001-choix-ollama.md` : décision de choisir Ollama

## Mode d'emploi

1. Lire `docs/installation.md` pour préparer l'environnement.
2. Consulter `docs/configuration.md` pour ajuster le comportement.
3. Utiliser `docs/monitoring.md` et `docs/governance.md` en production.
4. Se référer à `docs/operations.md` pour démarrer, arrêter et nettoyer.
