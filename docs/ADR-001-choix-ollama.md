# Architecture Decision Records

## ADR-001 : Choix d'Ollama comme LLM backend

**Statut** : Acceptée

### Contexte
ATLAS Consulting nécessite une solution 100% on-premise sans appel API externe.

### Décision
Nous utilisons **Ollama** pour :
- Exécuter des modèles open-source localement
- Zéro dépendance à des services cloud
- API REST simple et well-documented
- Support multi-plateforme (Windows, macOS, Linux)

### Conséquences
✅ Données clients sécurisées  
✅ Pas de coûts API récurrents  
⚠️ Limité par la RAM disponible localement  
⚠️ Vitesse dépend du CPU/GPU utilisateur
