import logging
import logging.handlers

log = logging.getLogger('music_notation')
log.setLevel(logging.DEBUG)

logfile = "./logs/music.log"
handler = logging.handlers.RotatingFileHandler(
    logfile, maxBytes=4*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s-%(levelname)s:%(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def log_info(info: str) -> None:
    log.info(info)


def log_debug(info: str) -> None:
    log.debug(info)


def log_warning(info: str) -> None:
    log.warning(info)
