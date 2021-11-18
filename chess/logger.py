import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument(
    "-log",
    "--loglevel",
    default="warning",
    help="Provide logging level. Example --loglevel debug, default=warning",
)

args = parser.parse_args()

loglevel = args.loglevel.upper()


def setlevel(logger, loglevel):
    if loglevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif loglevel == "INFO":
        logger.setLevel(logging.INFO)
    elif loglevel == "ERROR":
        logger.setLevel(logging.ERROR)
    elif loglevel == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.WARNING)
    return logger


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    blue = "\x1b[36m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# create logger with 'spam_application'
logger = logging.getLogger("Chess App")
logger = setlevel(logger, loglevel)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch = setlevel(ch, loglevel)

# add formatter to ch
ch.setFormatter(CustomFormatter())

# add ch to logger
logger.addHandler(ch)

if __name__ == "__main__":
    # 'application' code
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
