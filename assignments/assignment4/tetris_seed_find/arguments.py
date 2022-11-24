import argparse

parser = argparse.ArgumentParser(description='Play Tetris')
parser.add_argument(
    '--manual',
    '-m',
    default=False,
    action='store_true',
    help='Play manually'
)
# remove bellow line when submit
parser.add_argument("-f", "--fff", help="a dummy argument to fool ipython", default="1")

