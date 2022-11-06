"""

OwU's CLI

"""
import click
from owu import run, repl

@click.command()
@click.argument("files", type=click.STRING, nargs=-1)
@click.option("tree", "-t", type=click.BOOL, default=False, help="Print parsed tree of each line before evaling")
def main(files):
    if len(files) == 0:
        repl()
    else:
        for file in files:
            with open(file, "r") as f:
                run(f.read())

if __name__ == "__main__":
    main()
