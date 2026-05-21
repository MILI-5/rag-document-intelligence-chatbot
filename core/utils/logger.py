import logging


def get_logger(name="rag_app"):

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger(name)