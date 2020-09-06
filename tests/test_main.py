import logging
import main


def test_setup_logging_creates_rotating_file_handler():
    args = main.get_args()
    logger = main.setup_logging(args)
    assert type(logger.handlers[0]) is logging.handlers.RotatingFileHandler