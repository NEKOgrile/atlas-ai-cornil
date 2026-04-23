import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("logs/traces.jsonl", lines=True)

print("nb interactions:", len(df))

print("\nlatence moyenne:", int(df["latency_ms"].mean()), "ms")
print("latence médiane:", int(df["latency_ms"].median()), "ms")
print("latence p95:", int(df["latency_ms"].quantile(0.95)), "ms")

print("\nprompt tokens moyen:", int(df["prompt_tokens"].mean()))

print("\nplus lentes requêtes:")
print(df.sort_values("latency_ms", ascending=False)[["latency_ms", "user_message"]].head(5))


# 🔥 distribution tokens
plt.hist(df["prompt_tokens"], bins=10)
plt.title("distribution des tokens")
plt.show()


# 🔥 estimation coût GPT-4o (approx)
# prix approx: $5 / 1M tokens input, $15 / 1M output
input_cost = df["prompt_tokens"].sum() / 1_000_000 * 5
output_cost = df["completion_tokens"].sum() / 1_000_000 * 15

print("\ncout estimé GPT-4o:")
print("input:", round(input_cost, 4), "$")
print("output:", round(output_cost, 4), "$")
print("total:", round(input_cost + output_cost, 4), "$")