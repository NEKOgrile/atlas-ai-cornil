#!/usr/bin/env python3
"""
Script de test pour le client Ollama
Permet de vérifier que la connexion fonctionne et tester un chat simple
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from atlas.llm import OllamaClient


def test_connection():
    """Teste la connexion à Ollama"""
    print("Test de connexion a Ollama")
    client = OllamaClient()

    if not client.test_connection():
        print("Erreur : Impossible de se connecter a Ollama.")
        print("   - Verifiez qu'Ollama est installe : https://ollama.com/download")
        print("   - Lancez Ollama : ollama serve")
        print("   - Telechargez un modele : ollama pull llama3.2:3b")
        return False

    print("Connexion a Ollama reussie !")
    return True


def test_models():
    """Teste la récupération des modèles"""
    print("Recuperation des modeles disponibles")
    client = OllamaClient()
    models = client.get_available_models()

    if not models:
        print("Erreur : Aucun modele trouve.")
        print("   Telechargez un modele : ollama pull llama3.2:3b")
        return False

    print(f"Modeles disponibles : {', '.join(models)}")
    return True


def test_chat_simple():
    """Test un chat simple"""
    print("Test de chat simple")
    client = OllamaClient()

    # Message simple
    messages = [
        {"role": "user", "content": "Bonjour, peux-tu me dire ce qu'est Python en une phrase ?"}
    ]

    try:
        response = client.chat("llama3.2:3b", messages, stream=False)
        if response.get("success"):
            print(f"Reponse : {response['response']}")
            print(f"Tokens utilises : {response['metadata']['total_tokens']}")
            return True
        else:
            print(f"Erreur : {response.get('error')}")
            return False
    except Exception as e:
        print(f"Exception : {e}")
        return False


def test_chat_with_history():
    """Test un chat avec historique"""
    print("Test de chat avec historique")
    client = OllamaClient()

    # Historique de conversation
    history = [
        {"role": "user", "content": "Je m'appelle Alice et je travaille en IT."},
        {"role": "assistant", "content": "Bonjour Alice ! Ravi de vous rencontrer. En quoi puis-je vous aider avec vos projets IT ?"}
    ]

    user_message = "Quel est mon prénom ?"

    try:
        response = client.chat_with_history(
            "llama3.2:3b",
            user_message,
            history,
            system_prompt="Tu es un assistant helpful. Réponds en français."
        )

        if response.get("success"):
            print(f"Reponse : {response['response']}")
            print(f"Tokens utilises : {response['metadata']['total_tokens']}")
            return True
        else:
            print(f"Erreur : {response.get('error')}")
            return False
    except Exception as e:
        print(f"Exception : {e}")
        return False


def main():
    """Fonction principale"""
    print("Test du client Ollama ATLAS")
    print("=" * 50)

    # Tests séquentiels
    tests = [
        ("Connexion", test_connection),
        ("Modeles", test_models),
        ("Chat simple", test_chat_simple),
        ("Chat avec historique", test_chat_with_history)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"Erreur dans {name}: {e}")
            results.append((name, False))

    # Résumé
    print("\n" + "=" * 50)
    print("RESULTATS DES TESTS")
    print("=" * 50)

    passed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1

    print(f"\nTests reussis : {passed}/{len(results)}")

    if passed == len(results):
        print("Tous les tests sont passes ! Le client Ollama est pret.")
    else:
        print("Certains tests ont echoue. Verifiez votre installation d'Ollama.")


if __name__ == "__main__":
    main()