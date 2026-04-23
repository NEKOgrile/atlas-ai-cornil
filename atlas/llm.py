"""
Module wrapper pour l'API Ollama
Gère la communication avec les modèles LLM locaux
"""

import requests
import json
from typing import List, Dict, Any, Generator
import time


class OllamaClient:
    """Client pour communiquer avec l'API Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 300):
        """
        Initialise le client Ollama
        
        Args:
            base_url: URL de base pour l'API Ollama
            timeout: Timeout pour les requêtes en secondes
        """
        self.base_url = base_url
        self.timeout = timeout
    
    def get_available_models(self) -> List[str]:
        """Récupère la liste des modèles disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        except Exception as e:
            print(f"Erreur lors de la récupération des modèles: {e}")
            return []
    
    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        top_p: float = 0.9,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Envoie un message au modèle et reçoit une réponse
        
        Args:
            model: Nom du modèle à utiliser
            messages: Historique des messages
            temperature: Contrôle la créativité (0-1)
            top_p: Nucleus sampling parameter
            stream: Si True, retourne un generator pour le streaming
        
        Returns:
            Réponse du modèle
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._stream_response(response)
            else:
                return response.json()
        except requests.exceptions.Timeout:
            return {"error": f"Timeout après {self.timeout}s"}
        except Exception as e:
            return {"error": str(e)}
    
    def _stream_response(self, response) -> Generator:
        """Générateur pour le streaming de réponse"""
        for line in response.iter_lines():
            if line:
                yield json.loads(line)
