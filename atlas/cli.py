"""
CLI pour ATLAS - Interface en ligne de commande
(À développer au Sprint 1)
"""

import click


@click.group()
def cli():
    """ATLAS - Assistant IA Local"""
    pass


@cli.command()
@click.option("--model", default="llama3.2:3b", help="Modèle à utiliser")
@click.option("--temperature", default=0.3, help="Température (0-1)")
def chat(model: str, temperature: float):
    """Lance une session de chat interactif"""
    click.echo(f"Lancement du chat avec {model}...")
    # À développer au Sprint 1
    pass


if __name__ == "__main__":
    cli()
