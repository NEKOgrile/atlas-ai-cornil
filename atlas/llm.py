"""
Module wrapper pour l'API Ollama
Gère la communication avec les modèles LLM locaux
"""

import requests
import json
from typing import List, Dict, Any, Generator, Optional


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
        num_ctx: int = 4096,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Envoie un message au modèle et reçoit une réponse

        Args:
            model: Nom du modèle à utiliser
            messages: Historique des messages au format [{"role": "user", "content": "..."}]
            temperature: Contrôle la créativité (0-1)
            top_p: Nucleus sampling parameter
            num_ctx: Taille maximale du contexte
            stream: Si True, retourne un generator pour le streaming

        Returns:
            Réponse du modèle avec métadonnées
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "num_ctx": num_ctx,
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
                return self._handle_streaming_response(response)
            else:
                result = response.json()
                return self._format_response(result)

        except requests.exceptions.Timeout:
            return {
                "error": f"Timeout après {self.timeout}s",
                "success": False
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Impossible de se connecter à Ollama. Est-il démarré ?",
                "success": False
            }
        except Exception as e:
            return {
                "error": f"Erreur API: {str(e)}",
                "success": False
            }

    def _handle_streaming_response(self, response) -> Generator[Dict[str, Any], None, None]:
        """
        Gère la réponse en streaming

        Yields:
            Chunks de la réponse avec métadonnées
        """
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        full_response += content
                        yield {
                            "chunk": content,
                            "full_response": full_response,
                            "done": chunk.get('done', False),
                            "success": True
                        }
                    elif chunk.get('done', False):
                        # Message final avec métadonnées
                        yield {
                            "chunk": "",
                            "full_response": full_response,
                            "done": True,
                            "success": True,
                            "metadata": {
                                "prompt_tokens": chunk.get('prompt_eval_count', 0),
                                "completion_tokens": chunk.get('eval_count', 0),
                                "total_tokens": chunk.get('prompt_eval_count', 0) + chunk.get('eval_count', 0)
                            }
                        }
                except json.JSONDecodeError:
                    continue

    def _format_response(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formate la réponse de l'API Ollama

        Args:
            api_response: Réponse brute de l'API

        Returns:
            Réponse formatée avec métadonnées
        """
        message = api_response.get('message', {})
        return {
            "response": message.get('content', ''),
            "success": True,
            "model": api_response.get('model', ''),
            "metadata": {
                "prompt_tokens": api_response.get('prompt_eval_count', 0),
                "completion_tokens": api_response.get('eval_count', 0),
                "total_tokens": api_response.get('prompt_eval_count', 0) + api_response.get('eval_count', 0),
                "created_at": api_response.get('created_at', ''),
                "total_duration": api_response.get('total_duration', 0),
                "load_duration": api_response.get('load_duration', 0),
                "prompt_eval_duration": api_response.get('prompt_eval_duration', 0),
                "eval_duration": api_response.get('eval_duration', 0)
            }
        }

    def chat_with_history(
        self,
        model: str,
        user_message: str,
        history: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Envoie un message avec historique de conversation

        Args:
            model: Nom du modèle
            user_message: Message de l'utilisateur
            history: Historique des messages précédents
            system_prompt: Prompt système (optionnel)
            **kwargs: Paramètres supplémentaires pour chat()

        Returns:
            Réponse du modèle
        """
        # Construire la liste des messages
        messages = []

        # Ajouter le system prompt si fourni
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Ajouter l'historique
        messages.extend(history)

        # Ajouter le message actuel
        messages.append({"role": "user", "content": user_message})

        # Envoyer la requête
        return self.chat(model, messages, **kwargs)

    def test_connection(self) -> bool:
        """Teste la connexion à Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False