import argparse

from gendiff import generate_diff


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference.",
    )

    parser.add_argument("first_file")
    parser.add_argument("second_file")

    parser.add_argument(
        "-f",
        "--format",
        help="set format of output",
        metavar="FORMAT",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    format_name = args.format or "stylish"
    diff = generate_diff(
        args.first_file,
        args.second_file,
        format_name=format_name
    )
    print(diff)


if __name__ == "__main__":
    main()
