# Architecture ATLAS

## Vue d'ensemble

ATLAS est un assistant IA local construit pour répondre à des questions techniques, mémoriser des échanges et appliquer des règles métier sans appel à des APIs externes.

Les composants principaux sont :

- `atlas/llm.py` : client Ollama pour envoyer des requêtes `POST /api/chat`
- `atlas/memory.py` : mémoire courte et mémoire longue via ChromaDB
- `atlas/guardrails.py` : règles de sécurité et validation d'entrée
- `atlas/monitoring.py` : journalisation des interactions en JSONL
- `atlas/cli.py` : interface CLI principale
- `config/atlas.yaml` : configuration pilotée par Pydantic
- `Modelfile` : modèle Ollama custom utilisé en support

## Flux de données

1. L'utilisateur envoie un message dans la CLI.
2. `GuardrailsManager` vérifie la requête : PII, sujets bloqués, longueur, prompt injection, rate limit.
3. Le message est nettoyé et le system prompt est ajouté.
4. La mémoire longue recherche des souvenirs pertinents et les injecte dans le prompt.
5. La requête est envoyée à Ollama.
6. La réponse est renvoyée au CLI, enregistrée dans l'historique court et éventuellement stockée en mémoire longue.
7. Une trace JSON est écrite dans `logs/traces.jsonl`.

## Composants

- `atlas_chat.py` : point d'entrée CLI.
- `atlas/cli.py` : lance la boucle interactive et gère les options.
- `atlas/llm.py` : wrapper Ollama, gestion des erreurs et streaming.
- `atlas/memory.py` : gestion de la mémoire courte et longue.
- `atlas/monitoring.py` : logger des traces.
- `atlas/guardrails.py` : règles de sécurité.
- `config/atlas.yaml` : configuration du modèle, persona, mémoire et guardrails.
- `Modelfile` : modèle Ollama custom.

## Decisions

### System prompt

On a choisi de mettre le system prompt dans le YAML et non seulement dans le Modelfile.

Raison : c'est plus simple à modifier et permet de changer de comportement sans recréer un modèle Ollama.

---

### YAML vs Modelfile

Modifier le YAML sans toucher au Modelfile peut créer des incohérences.

Le Modelfile est un support, mais le comportement principal vient de la configuration du code.

---

### Choix du modèle dans la CLI

La CLI utilise le modèle configuré dans `config/atlas.yaml` plutôt qu'un modèle custom fixe.

Avantages : plus de flexibilité, moins de maintenance et un prototype plus agile.

---

### Conclusion

La conception privilégie la simplicité, la flexibilité et la transparence côté code, ce qui est adapté à un prototype local et à un livrable rapide.