#!/usr/bin/env python3
"""
Script de lancement pour la CLI ATLAS
Permet de lancer atlas-chat depuis la racine du projet
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importer et lancer la CLI
from atlas.cli import cli

if __name__ == "__main__":
    cli()