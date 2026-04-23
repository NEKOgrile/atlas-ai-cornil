# Opérations

Guide d'exploitation du projet ATLAS.

## Démarrage

1. Activer l'environnement Python :

```bash
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

2. Vérifier Ollama :

```bash
curl http://localhost:11434/api/tags
```

3. Lancer le chat :

```bash
python atlas_chat.py chat
```

## Commandes utiles

- `quit`, `exit`, `q` : quitter le chat
- `clear`, `cls` : effacer l'historique
- `help` : afficher l'aide

## Maintenance

### Réinitialiser la mémoire courte

Redémarrer le chat suffit à vider la mémoire courte.

### Purger la mémoire longue

Supprimer le dossier de mémoire ChromaDB :

```bash
rm -rf data/memory
```

### Purger les traces

```bash
rm logs/traces.jsonl
```

## Sauvegarde

- `data/memory` : souvenirs persistants
- `logs/traces.jsonl` : historique de trace

## Débogage

### Vérifier la config

Ouvrir `config/atlas.yaml` pour s'assurer que le fichier est valide.

### Tester la connexion Ollama

```bash
python -c "from atlas.llm import OllamaClient; print(OllamaClient().test_connection())"
```

### Exécuter les tests

```bash
pytest
```

## Rollback

Si un changement cause un problème, revenir à la version précédente avec Git :

```bash
git checkout -- .
``` 

ou

```bash
git reset --hard HEAD~1
```
