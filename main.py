from argparse import ArgumentParser

from visualizer import Visualizer


def main():
    parser = ArgumentParser()
    parser.add_argument(dest="csv", nargs="?")
    args = parser.parse_args()
    visualizer = Visualizer(args.csv)
    visualizer.run()


if __name__ == "__main__":
    main()
