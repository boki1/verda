import logging
from script_reader import PhraseParser


def setup_logging():
    format_str = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=format_str, filename="output.log", level=logging.DEBUG)


def main():
    setup_logging()

    verda = PhraseParser()
    verda.get_from_file("../../misc/eco.phrases")
    print(verda)


if __name__ == "__main__":
    main()
