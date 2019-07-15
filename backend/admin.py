import sqlite3
import logging
from functools import partial, wraps


def connect(path_to_db, verbose=False):
    try:
        db = sqlite3.connect(path_to_db)

        # Apply pragma to enforce foreign keys
        db.execute('pragma foreign_keys = 1;')

        return db

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception('Unable to connect to db', exc_info=e)
        if verbose:
            msg = "Unable to open db: {} Error: {} reason: {}. Probably missing folder or insufficient permission"
            raise RuntimeError(msg.format(path_to_db, e.__class__.__name__, e))


def initialise(path_to_db, verbose=False):
    from os.path import split
    from os.path import join
    from os.path import expanduser
    from os import mkdir
    from os.path import exists
    home, _ = split(path_to_db)
    home = expanduser(home)
    if not exists(home):
        mkdir(home)
    path_to_db = join(home, _)
    connect(path_to_db, verbose=verbose)
    return path_to_db


def connection(func=None):
    if func is None:
        return partial(connection)

    @wraps(func)
    def wrapper(*args, **kwargs):

        conn = args[0] if args else None
        if isinstance(conn, str):
            conn = connect(conn)

        return func(conn, *args[1:], **kwargs)

    return wrapper
