
class Logger:
    def info(self, mess):
        print('\n', '!!! LOGGER INFO: {0}'.format(mess), '\n')

    def error(self, mess):
        print('\n', '!!! LOGGER ERROR: {0}'.format(mess), '\n')

logger = Logger()

def logged(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('Enter to function {0}'.format(repr(func)))
        result = func(*args, **kwargs)
        logger.info('Exit from function {0}'.format(repr(func)))

        return result

    return wrapper
