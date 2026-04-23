import re
import time


class GuardrailsManager:

    def __init__(self, config=None):
        config = config or {}

        self.enabled = config.get("enabled", True)
        self.blocked_topics = config.get("blocked_topics", [])
        self.max_length = config.get("max_length", 50)

        self.rate_limit = config.get("rate_limit", 10)
        self.timestamps = []

    def apply_input_guardrails(self, text):

        if not self.enabled:
            return text, []

        rules = []

        # 🔥 1. PII (carte bancaire simple)
        if re.search(r"\b\d{16}\b", text):
            text = re.sub(r"\b\d{16}\b", "[CB_MASKED]", text)
            rules.append("pii_mask")

        # 🔥 2. sujets interdits
        for topic in self.blocked_topics:
            if topic in text.lower():
                rules.append("blocked_topic")
                return "sujet bloqué", rules

        # 🔥 3. longueur
        if len(text.split()) > self.max_length:
            rules.append("too_long")
            return "message trop long", rules

        # 🔥 4. prompt injection
        if any(x in text.lower() for x in ["ignore previous", "tu es maintenant", "<|system|>"]):
            rules.append("prompt_injection")
            return "tentative refusée", rules

        # 🔥 5. rate limit
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < 60]

        if len(self.timestamps) >= self.rate_limit:
            rules.append("rate_limit")
            return "trop de requêtes", rules

        self.timestamps.append(now)

        return text, rules