"""Console script for rogi_rl."""
import sys
import click


@click.command()
@click.option('--width',
              default=50,
              help="Width of the Grid"
              )
@click.option('--height',
              default=50,
              help="Height of the Grid"
              )
def demo(width, height):
    """
    Demo script to test installation
    """
    from rogi_rl.server import build_server  # noqa

    server = build_server(width, height)
    server.launch()


if __name__ == "__main__":
    sys.exit(demo())  # pragma: no cover
