from logging import INFO, basicConfig

from lib import parse_args


def main() -> None:
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    options = parse_args()


if __name__ == "__main__":
    main()
