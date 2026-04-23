# 🏢 ATLAS — Assistant IA Local

Assistant IA 100% on-premise pour ATLAS Consulting, construit en une journée.

## 🎯 Objectif

Fournir aux consultants un assistant IA local qui :
- Répond à des questions techniques
- Mémorise les échanges précédents
- Respecte des règles de confidentialité (pas de fuites de données client)
- Fonctionne entièrement on-premise (zero données envoyées à OpenAI/Anthropic)

## 🚀 Démarrage rapide

### Prérequis
- Python 3.10+
- Ollama (https://ollama.com/download)
- 8 Go de RAM minimum

### Installation

1. **Cloner le repo** :
```bash
cd atlas-ai-cornil
```

2. **Créer un environnement virtuel** :
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances** :
```bash
pip install -e .
```

4. **Télécharger un modèle Ollama** :
```bash
ollama pull llama3.2:3b
# Ou selon votre RAM :
# - 16 Go : ollama pull qwen3:8b
# - < 8 Go : ollama pull gemma3:1b
```

5. **Vérifier que Ollama tourne** :
```bash
curl http://localhost:11434/api/tags
```

6. **Lancer l'assistant** :
```bash
# Activer l'environnement virtuel
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Lancer le chat interactif
python atlas_chat.py chat

# Options disponibles :
python atlas_chat.py chat --help
```

### Utilisation du chat

Une fois lancé, vous pouvez discuter avec Atlas :

```
🤖 Bienvenue dans ATLAS - Assistant IA Local
📚 Modèle: llama3.2:3b
🌡️  Température: 0.3
🛡️  Guardrails: Activés
--------------------------------------------------
Vous: Bonjour Atlas !
🤖 Atlas: Bonjour ! Je suis Atlas, votre assistant IA. Comment puis-je vous aider ?
Vous: Quelles sont tes fonctionnalités ?
🤖 Atlas: Je peux vous aider avec des questions techniques, la documentation, l'organisation de projets...
Vous: quit
👋 Au revoir !
```

**Commandes spéciales :**
- `quit` / `exit` / `q` : Quitter la session
- `clear` / `cls` : Effacer l'historique
- `help` : Afficher l'aide

**Options CLI :**
- `--model MODEL` : Changer de modèle
- `--temperature TEMP` : Ajuster la créativité (0-1)
- `--system-prompt PROMPT` : Prompt système personnalisé
- `--no-guardrails` : Désactiver les règles de sécurité

## 📁 Structure du projet

```
atlas-ai-cornil/
├── atlas/              # Package principal
│   ├── __init__.py
│   ├── llm.py         # Client Ollama
│   ├── memory.py      # Gestion mémoire (court & long terme)
│   ├── monitoring.py  # Traçabilité des interactions
│   └── guardrails.py  # Règles de sécurité
├── config/            # Fichiers de configuration
├── data/              # Données persistantes
├── scripts/           # Scripts utilitaires
├── tests/             # Tests unitaires
├── docs/              # Documentation
├── .gitignore
├── pyproject.toml     # Dépendances Python
└── README.md
```

## 📊 Sprints

- **Sprint 0** : Kickoff (en cours)
- **Sprint 1** : CLI fonctionnelle
- **Sprint 2** : Mémoire vectorielle
- **Sprint 3** : Monitoring & guardrails
- **Sprint 4** : Configuration & personnalisation
- **Sprint 5** : Documentation

## 👥 Équipe

- **Cornil** : Développement principal

## 🔗 Ressources

- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [ChromaDB](https://docs.trychroma.com)
- [Langfuse](https://langfuse.com)

## 📝 Licence

Projet académique — ATLAS Consulting
