import logging

def get_logger(nombre,archivo='debug.log'):
    log = logging.getLogger(nombre)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(archivo)
    frm = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
    fh.setFormatter(frm)
    log.addHandler(fh)
    return log
