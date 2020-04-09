"""Console script for rogi_rl."""
import sys
import click


@click.command()
def demo(args=None):
    """
    Demo script to test installation
    """
    from rogi_rl.server import server  # noqa
    server.launch()


if __name__ == "__main__":
    sys.exit(demo())  # pragma: no cover
