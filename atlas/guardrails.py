"""
Module de gouvernance et guardrails
Applique des règles de sécurité et de politique aux interactions
"""

import re
from typing import Tuple, Dict, List


class GuardrailsManager:
    """Gère les guardrails et règles de sécurité"""
    
    def __init__(self, config: Dict = None):
        """
        Initialise le manager
        
        Args:
            config: Configuration des règles
        """
        self.config = config or {}
        self.blocked_topics = self.config.get("blocked_topics", [])
        self.enabled = self.config.get("enabled", True)
    
    def apply_input_guardrails(self, user_message: str) -> Tuple[str, List[str]]:
        """
        Applique les guardrails à l'entrée
        
        Returns:
            Tuple (message modifié, liste des règles déclenchées)
        """
        if not self.enabled:
            return user_message, []
        
        triggered_rules = []
        modified_message = user_message
        
        # Détection de PII - numéro de carte
        if self._contains_credit_card(user_message):
            modified_message = self._mask_credit_cards(modified_message)
            triggered_rules.append("credit_card_detected")
        
        # Détection d'email
        if self._contains_email(user_message):
            modified_message = self._mask_emails(modified_message)
            triggered_rules.append("email_detected")
        
        # Vérification des sujets bloqués
        if self._contains_blocked_topic(user_message):
            triggered_rules.append("blocked_topic")
        
        # Détection de prompt injection
        if self._contains_prompt_injection(user_message):
            triggered_rules.append("prompt_injection_detected")
        
        return modified_message, triggered_rules
    
    def _contains_credit_card(self, text: str) -> bool:
        """Détecte un numéro de carte de crédit"""
        # Luhn algorithm check
        pattern = r'\b(?:\d{4}[\s-]?){3}\d{4}\b'
        return bool(re.search(pattern, text))
    
    def _mask_credit_cards(self, text: str) -> str:
        """Masque les numéros de carte"""
        pattern = r'\b(?:\d{4}[\s-]?){3}\d{4}\b'
        return re.sub(pattern, '[CREDIT_CARD_MASKED]', text)
    
    def _contains_email(self, text: str) -> bool:
        """Détecte un email"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return bool(re.search(pattern, text))
    
    def _mask_emails(self, text: str) -> str:
        """Masque les emails"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(pattern, '[EMAIL_MASKED]', text)
    
    def _contains_blocked_topic(self, text: str) -> bool:
        """Vérifie la présence de sujets bloqués"""
        text_lower = text.lower()
        return any(topic.lower() in text_lower for topic in self.blocked_topics)
    
    def _contains_prompt_injection(self, text: str) -> bool:
        """Détecte les tentatives d'injection de prompt"""
        injection_patterns = [
            r'ignore previous instructions',
            r'tu es maintenant',
            r'<\|system\|>',
            r'forget all previous',
            r'override the system'
        ]
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in injection_patterns)
