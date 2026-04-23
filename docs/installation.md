# Installation

## Prérequis

- Python 3.10+
- Ollama installé et en cours d'exécution
- 8 Go de RAM minimum
- Git

## 1. Cloner le dépôt

```bash
cd "c:\Users\thebe\Documents\cours\M1\IA outils de développement"
git clone https://github.com/NEKOgrile/atlas-ai-cornil.git
cd atlas-ai-cornil
```

## 2. Créer l'environnement Python

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

## 3. Installer les dépendances

```bash
pip install -e .
```

## 4. Télécharger un modèle Ollama

```bash
ollama pull llama3.2:3b
```

Alternatives selon la RAM :

- 16 Go : `ollama pull qwen3:8b`
- < 8 Go : `ollama pull gemma3:1b`

## 5. Vérifier Ollama

```bash
curl http://localhost:11434/api/tags
```

Si la commande renvoie la liste des modèles, Ollama est prêt.

## 6. Lancer le chat

```bash
python atlas_chat.py chat
```

### Notes

- Si `config/atlas.yaml` est manquant ou invalide, le CLI échoue avec un message clair.
- Le projet inclut un `Modelfile` pour un modèle Ollama custom à partir de `models/atlas-tuned.gguf`.
