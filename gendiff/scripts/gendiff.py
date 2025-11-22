import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    return parser


def main() -> None:
    parser = build_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()
