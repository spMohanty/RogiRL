"""Console script for rog_rl."""
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
    from rog_rl.server import build_server  # noqa

    server = build_server(width, height)
    server.launch()


@click.command(name="profile-perf")
@click.option('-ron/-rof', '--render_on/--render_off',
              default=False,
              help="If render profiling required"
              )
def profile_perf(render_on):
    """
    Run script to obtain performance metrics.
    If render profile is required, it saves a file `profile_stats_render`
    It also prints the output of the profiling sorted by cumulative time
    """
    from rog_rl.benchmark import performance_metrics

    performance_metrics(render_on)


if __name__ == "__main__":
    sys.exit(demo())  # pragma: no cover
