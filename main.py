"""

OwU's CLI

"""
import click
from owu import run, repl

@click.command()
@click.argument("files", type=click.STRING, nargs=-1)
def main(files):
    if len(files) == 0:
        repl()
    else:
        for file in files:
            with open(file, "r") as f:
                run(f.read())

if __name__ == "__main__":
    main()
