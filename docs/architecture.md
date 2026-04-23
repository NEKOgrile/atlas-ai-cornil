## Decisions

### System prompt

on a choisi de mettre le system prompt dans le code (via le YAML) et pas dans le Modelfile

raison : c’est beaucoup plus simple à modifier, pas besoin de recréer un modèle Ollama à chaque changement  
ça permet de tester rapidement différents comportements sans toucher au modèle

---

### YAML vs Modelfile

si quelqu’un modifie le YAML mais pas le Modelfile, ça peut créer des incohérences  
le modèle peut suivre le prompt du Modelfile au lieu de celui du code

du coup comportement pas clair + difficile à debug

---

### Choix du modèle dans la CLI

la CLI pointe vers le modèle de base (llama / mistral) et pas vers un modèle custom `atlas`

le system prompt est injecté côté code

raison :
- plus flexible
- pas besoin de maintenir plusieurs modèles
- plus simple pour un prototype

---

### Conclusion

on privilégie la simplicité et la flexibilité côté code plutôt qu’un modèle figé dans Ollama  
c’est plus adapté pour du dev rapide et des tests