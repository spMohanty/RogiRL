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


@click.command()
@click.option('-p/-np', '--profile-render/--no-profile-render',
              default=False,
              help="If render profiling required"
              )
def profile_perf(profile_render):
    """
    Run script to obtain performance metrics.
    If render profile is required, it saves a file `profile_stats_render`
    It also prints the output of the profiling sorted by cumulative time
    """
    from rogi_rl.benchmark import performance_metrics

    performance_metrics(profile_render)


if __name__ == "__main__":
    sys.exit(demo())  # pragma: no cover
