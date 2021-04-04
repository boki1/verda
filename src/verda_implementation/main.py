import logging
from .engine import VerdaEngine


def setup_logging():
    format_str = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=format_str, filename="output.log", level=logging.DEBUG)


def main():
    setup_logging()

    verda_engine = VerdaEngine()
    verda_engine.loop()


if __name__ == "__main__":
    main()
