#!/usr/bin/env python3
"""
Script d'analyse des traces (Sprint 3)
Génère des statistiques sur les interactions LLM
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_traces(log_path: str) -> List[Dict[str, Any]]:
    """Charge les traces JSONL"""
    traces = []
    log_file = Path(log_path)
    
    if not log_file.exists():
        print(f"Fichier de traces non trouvé: {log_path}")
        return traces
    
    with open(log_file, "r") as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))
    
    return traces


def analyze_traces(traces: List[Dict]) -> None:
    """Analyse les traces et affiche les statistiques"""
    if not traces:
        print("Aucune trace à analyser")
        return
    
    print("=" * 60)
    print("ANALYSE DES TRACES ATLAS")
    print("=" * 60)
    
    # Statistiques basiques
    latencies = [t.get("latency_ms", 0) for t in traces]
    prompt_tokens = [t.get("prompt_tokens", 0) for t in traces]
    completion_tokens = [t.get("completion_tokens", 0) for t in traces]
    
    print(f"\nNombre d'interactions: {len(traces)}")
    print(f"\nLatence (ms):")
    print(f"  - Min: {min(latencies):.0f}")
    print(f"  - Max: {max(latencies):.0f}")
    print(f"  - Moyenne: {sum(latencies)/len(latencies):.0f}")
    
    print(f"\nTokens:")
    print(f"  - Prompt total: {sum(prompt_tokens)}")
    print(f"  - Completion total: {sum(completion_tokens)}")
    print(f"  - Moyenne prompt: {sum(prompt_tokens)/len(traces):.0f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    log_path = "./logs/traces.jsonl"
    traces = load_traces(log_path)
    analyze_traces(traces)
