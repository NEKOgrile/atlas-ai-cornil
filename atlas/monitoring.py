"""
Module de monitoring et de traçabilité
Enregistre les interactions pour analyse et audit
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from functools import wraps


class TraceLogger:
    """Enregistre les traces structurées en JSONL"""
    
    def __init__(self, log_path: str = "./logs/traces.jsonl"):
        """
        Initialise le logger
        
        Args:
            log_path: Chemin du fichier de traces
        """
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_interaction(
        self,
        session_id: str,
        model: str,
        user_message: str,
        assistant_message: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        latency_ms: float = 0,
        memory_hits: int = 0,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Enregistre une interaction
        
        Args:
            session_id: ID unique de la session
            model: Modèle utilisé
            user_message: Message de l'utilisateur
            assistant_message: Réponse du modèle
            prompt_tokens: Nombre de tokens en entrée
            completion_tokens: Nombre de tokens en sortie
            latency_ms: Latence en millisecondes
            memory_hits: Nombre de souvenirs injectés
            metadata: Métadonnées supplémentaires
        """
        trace = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "model": model,
            "user_message": user_message[:200],  # Truncate pour la vie privée
            "assistant_message": assistant_message[:200],
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "latency_ms": latency_ms,
            "memory_hits": memory_hits,
            "metadata": metadata or {}
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(trace) + "\n")


def traced(logger, session_id, model, memory_hits=0):

    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            result = func(*args, **kwargs)

            latency = (time.perf_counter() - start) * 1000

            try:
                metadata = result.get("metadata", {})
                user_message = kwargs.get("user_message", "")
                assistant_message = result.get("response", "")

                logger.log_interaction(
                    session_id=session_id,
                    model=model,
                    user_message=user_message,
                    assistant_message=assistant_message,
                    prompt_tokens=metadata.get("prompt_tokens", 0),
                    completion_tokens=metadata.get("completion_tokens", 0),
                    latency_ms=latency,
                    memory_hits=memory_hits
                )
            except Exception as e:
                print("trace error:", e)

            return result

        return wrapper

    return decorator
