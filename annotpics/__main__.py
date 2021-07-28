import sys
import click

from .interface import AnnotationInterfacsdfijhse

@click.version_option("0.0.1")
@click.command()
@click.argument('csv', required=True)
@click.argument('image_dir', required=True)
@click.argument('bindings', required=True)
@click.option('--start_i', default=1, required=False)
@click.option('--window_w', default=764, required=False)
@click.option('--window_h', default=1200, required=False)

def main(csv, image_dir, bindings, start_i, 
         window_w, window_h):
    r"""
    EXPERIMENTAL
    Picture annotation tool.
    """
    print("csv =", csv)
    print("image_dir=", image_dir)
    print("bindings =", bindings)
    print("start_i =", start_i)
    print("window_w =", window_w)
    print("window_h =", window_h)

    pass


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Picture annotation tool")
    main()
