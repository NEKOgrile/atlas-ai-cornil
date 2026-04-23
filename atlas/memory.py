"""
Module de gestion de la mémoire (courte et longue terme)
Utilise ChromaDB pour la mémoire vectorielle persistante
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class ShortTermMemory:
    """Gestion de la mémoire courte (session actuelle)"""
    
    def __init__(self, max_messages: int = 50):
        """
        Initialise la mémoire courte
        
        Args:
            max_messages: Nombre maximum de messages à garder
        """
        self.messages: List[Dict[str, str]] = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str) -> None:
        """Ajoute un message à l'historique"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Garder seulement les N derniers messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_history(self) -> List[Dict[str, str]]:
        """Retourne l'historique des messages"""
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    
    def clear(self) -> None:
        """Efface l'historique"""
        self.messages = []


class LongTermMemory:
    """Gestion de la mémoire longue (persistante entre sessions)"""
    
    def __init__(self, db_path: str = "./data/memory"):
        """
        Initialise la mémoire longue
        
        Args:
            db_path: Chemin vers la base de données ChromaDB
        """
        self.db_path = db_path
        # ChromaDB sera initialisé au Sprint 2
        self.memories: List[Dict[str, Any]] = []
    
    def store_memory(self, content: str, metadata: Optional[Dict] = None) -> None:
        """Stocke un souvenir"""
        memory = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.memories.append(memory)
    
    def search_memories(self, query: str, top_k: int = 5) -> List[Dict]:
        """Cherche des souvenirs pertinents"""
        # Sera implémenté avec ChromaDB au Sprint 2
        return []
    
    def get_all_memories(self) -> List[Dict]:
        """Retourne tous les souvenirs"""
        return self.memories
