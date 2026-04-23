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
    print("🔍 Test de connexion à Ollama...")
    client = OllamaClient()

    if not client.test_connection():
        print("❌ Impossible de se connecter à Ollama.")
        print("   - Vérifiez qu'Ollama est installé : https://ollama.com/download")
        print("   - Lancez Ollama : ollama serve")
        print("   - Téléchargez un modèle : ollama pull llama3.2:3b")
        return False

    print("✅ Connexion à Ollama réussie!")
    return True


def test_models():
    """Teste la récupération des modèles"""
    print("\n📋 Récupération des modèles disponibles...")
    client = OllamaClient()
    models = client.get_available_models()

    if not models:
        print("❌ Aucun modèle trouvé.")
        print("   Téléchargez un modèle : ollama pull llama3.2:3b")
        return False

    print(f"✅ Modèles disponibles : {', '.join(models)}")
    return True


def test_chat_simple():
    """Test un chat simple"""
    print("\n💬 Test de chat simple...")
    client = OllamaClient()

    # Message simple
    messages = [
        {"role": "user", "content": "Bonjour, peux-tu me dire ce qu'est Python en une phrase ?"}
    ]

    try:
        response = client.chat("llama3.2:3b", messages, stream=False)
        if response.get("success"):
            print(f"🤖 Réponse : {response['response']}")
            print(f"📊 Tokens utilisés : {response['metadata']['total_tokens']}")
            return True
        else:
            print(f"❌ Erreur : {response.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Exception : {e}")
        return False


def test_chat_with_history():
    """Test un chat avec historique"""
    print("\n📚 Test de chat avec historique...")
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
            print(f"🤖 Réponse : {response['response']}")
            print(f"📊 Tokens utilisés : {response['metadata']['total_tokens']}")
            return True
        else:
            print(f"❌ Erreur : {response.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Exception : {e}")
        return False


def main():
    """Fonction principale"""
    print("🚀 Test du client Ollama ATLAS")
    print("=" * 50)

    # Tests séquentiels
    tests = [
        ("Connexion", test_connection),
        ("Modèles", test_models),
        ("Chat simple", test_chat_simple),
        ("Chat avec historique", test_chat_with_history)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erreur dans {name}: {e}")
            results.append((name, False))

    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 50)

    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1

    print(f"\nTests réussis : {passed}/{len(results)}")

    if passed == len(results):
        print("🎉 Tous les tests sont passés ! Le client Ollama est prêt.")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez votre installation d'Ollama.")


if __name__ == "__main__":
    main()