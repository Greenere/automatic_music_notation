import logging
import logging.handlers

log = logging.getLogger('music_notation')
log.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler('music.log', maxBytes=4*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s-%(levelname)s:%(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

def log_info(info):
    log.info(info)

def log_debug(info):
    log.debug(info)

def log_warning(info):
    log.warning(info)