from logging import INFO, basicConfig


def main() -> None:
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


if __name__ == "main":
    main()
