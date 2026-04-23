"""
atlas cli (vite fait)
"""

import sys
import yaml
from pathlib import Path
import time
import uuid

import click

from atlas.config.schema import AtlasConfig
from .llm import OllamaClient
from .guardrails import GuardrailsManager
from .memory import LongTermMemory
from .monitoring import TraceLogger


def load_config():
    path = Path(__file__).parent.parent / "config" / "atlas.yaml"

    if not path.exists():
        click.echo("config introuvable...")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return AtlasConfig(**data)
    except Exception as e:
        click.echo(f"erreur config: {e}")
        return None


@click.group()
def cli():
    pass


def count_tokens(messages):
    text = ""
    for m in messages:
        text += m["content"] + " "
    return int(len(text.split()) * 1.3)


@cli.command()
@click.option("--model")
@click.option("--temperature", type=float)
@click.option("--system-prompt")
@click.option("--no-guardrails", is_flag=True)
def chat(model, temperature, system_prompt, no_guardrails):

    config = load_config()

    if not config:
        click.echo("config invalide")
        return

    # 🔥 CONFIG CLEAN
    model_name = model or config.model.name
    temp = temperature if temperature is not None else config.model.temperature
    sys_prompt = system_prompt or config.persona.system_prompt

    try:
        client = OllamaClient(
            timeout=config.model.timeout
        )

        # 🔥 guardrails config
        guardrails_config = {
            "enabled": config.guardrails.enabled,
            "blocked_topics": config.guardrails.blocked_topics
        }

        if no_guardrails:
            guardrails_config["enabled"] = False

        guardrails = GuardrailsManager(guardrails_config)

        mem = LongTermMemory()
        logger = TraceLogger()
        session_id = str(uuid.uuid4())

        click.echo("\natlas lancé")
        click.echo(f"model: {model_name}")
        click.echo(f"temp: {temp}")
        click.echo(f"guardrails: {'on' if guardrails.enabled else 'off'}")
        click.echo("quit pour sortir\n")

        history = []

        while True:
            try:
                msg = click.prompt("toi")

                if msg.lower() in ["quit", "exit", "q"]:
                    break

                if msg.lower() in ["clear", "cls"]:
                    history = []
                    click.echo("reset")
                    continue

                if msg.lower() == "help":
                    click.echo("quit / clear / help")
                    continue

                cleaned, rules = guardrails.apply_input_guardrails(msg)

                if rules:
                    click.echo(f"rules: {rules}")

                messages = []

                if sys_prompt:
                    messages.append({"role": "system", "content": sys_prompt})

                messages += history

                # 🔥 mémoire
                mems = mem.search(cleaned, k=3)

                if mems:
                    context = "\n".join(mems)
                    messages.append({
                        "role": "system",
                        "content": f"infos utilisateur:\n{context}"
                    })

                messages.append({"role": "user", "content": cleaned})

                # tokens
                tokens = count_tokens(messages)
                click.echo(f"[tokens] {tokens}")

                # appel modèle + timer
                start = time.perf_counter()

                res = client.chat(
                    model=model_name,
                    messages=messages,
                    temperature=temp,
                    stream=False
                )

                latency = (time.perf_counter() - start) * 1000

                if res.get("success"):
                    out = res["response"]
                    click.echo(f"atlas: {out}")

                    history.append({"role": "user", "content": cleaned})
                    history.append({"role": "assistant", "content": out})

                    # 🔥 stockage mémoire
                    if any(x in cleaned.lower() for x in ["je suis", "je m'appelle", "je bosse", "travaille"]):
                        mem.store(cleaned)

                    # 🔥 LOG
                    metadata = res.get("metadata", {})

                    logger.log_interaction(
                        session_id=session_id,
                        model=model_name,
                        user_message=cleaned,
                        assistant_message=out,
                        prompt_tokens=metadata.get("prompt_tokens", tokens),
                        completion_tokens=metadata.get("completion_tokens", 0),
                        latency_ms=latency,
                        memory_hits=len(mems)
                    )

                    # 🔥 mémoire courte
                    max_h = config.memory.max_short_term
                    if len(history) > max_h * 2:
                        history = history[-max_h * 2:]

                else:
                    click.echo(f"erreur: {res.get('error')}")

            except KeyboardInterrupt:
                break
            except Exception as e:
                click.echo(f"erreur: {e}")

    except Exception as e:
        click.echo(f"init cassée: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()