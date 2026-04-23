from pydantic import BaseModel
from typing import List


class ModelConfig(BaseModel):
    name: str
    temperature: float
    top_p: float
    num_ctx: int


class PersonaConfig(BaseModel):
    name: str
    system_prompt: str


class MemoryConfig(BaseModel):
    top_k: int
    min_similarity: float


class GuardrailsConfig(BaseModel):
    enabled: bool
    blocked_topics: List[str]


class AtlasConfig(BaseModel):
    model: ModelConfig
    persona: PersonaConfig
    memory: MemoryConfig
    guardrails: GuardrailsConfig