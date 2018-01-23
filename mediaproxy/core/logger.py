import os
import sys
import logging
import logging.handlers

class Logger:

    def __init__(self, formatter=None):

        fmt_string = "[%(levelname)-7s] (%(name)s) %(asctime)s.%(msecs)-3d Thread:%(thread)s/%(module)s[%(lineno)-3d]/%(funcName)-10s  %(message)-8s "
        self.formatter = logging.Formatter(fmt_string, " %d.%m.%Y %H:%M:%S")

    def create_stream_logger(self, loggername=None, level=3, stream=None, **kwargs):

        if 'handlername' in kwargs:
            handlername = kwargs['handlername']
        else:
            handlername='stdout'

        if 'formatter' in kwargs:
            formatter = kwargs['formatter']
        else:
            formatter=self.formatter

        if loggername is None:
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(loggername)

        if not 0 < level < 6:
            return logger

        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            if handler.get_name() == handlername:
                return
        if stream:
            handler = logging.StreamHandler(stream)
        else:
            handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler.set_name(handlername)

        if level == 1:
            handler.setLevel(logging.DEBUG)
        if level == 2:
            handler.setLevel(logging.INFO)
        if level == 3:
            handler.setLevel(logging.WARNING)
        if level == 4:
            handler.setLevel(logging.ERROR)
        if level == 5:
            handler.setLevel(logging.CRITICAL)

        logger.addHandler(handler)

    def create_file_logger(self, path, loggername=None, level=1, **kwargs):

        if 'handlername' in kwargs:
            handlername = kwargs['handlername']
        else:
            handlername='file'

        if 'formatter' in kwargs:
            formatter = kwargs['formatter']
        else:
            formatter=self.formatter

        if loggername is None:
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(loggername)

        if not 0 < level < 6:
            return logger

        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            if handler.get_name() == handlername:
                return

        handler = logging.FileHandler(path)
        handler.setFormatter(formatter)
        handler.set_name(handlername)

        if level == 1:
            handler.setLevel(logging.DEBUG)
        if level == 2:
            handler.setLevel(logging.INFO)
        if level == 3:
            handler.setLevel(logging.WARNING)
        if level == 4:
            handler.setLevel(logging.ERROR)
        if level == 5:
            handler.setLevel(logging.CRITICAL)

        logger.addHandler(handler)

    def create_rotating_file_logger(self, path, loggername=None, level=1, **kwargs):

        if 'handlername' in kwargs:
            handlername = kwargs['handlername']
        else:
            handlername='rotate_file'

        if 'max_bytes' in kwargs:
            max_bytes = kwargs['max_bytes']
        else:
            max_bytes = 1024 * 1024

        if 'backup_count' in kwargs:
            backup_count = kwargs['backup_count']
        else:
            backup_count = 10

        if loggername is None:
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(loggername)

        if not 0 < level < 6:
            return logger

        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            if handler.get_name() == handlername:
                return

        handler = logging.handlers.RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(self.formatter)
        handler.set_name(handlername)

        if level == 1:
            handler.setLevel(logging.DEBUG)
        if level == 2:
            handler.setLevel(logging.INFO)
        if level == 3:
            handler.setLevel(logging.WARNING)
        if level == 4:
            handler.setLevel(logging.ERROR)
        if level == 5:
            handler.setLevel(logging.CRITICAL)

        logger.addHandler(handler)

    def create_local_syslog_logger(self, loggername=None, level=0, **kwargs):

        if 'handlername' in kwargs:
            handlername = kwargs['handlername']
        else:
            handlername='syslog'

        if loggername is None:
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(loggername)
            
        if not 0 < level < 6:
            return logger

        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers:
            if handler.get_name() == handlername:
                return

        handler = logging.handlers.SysLogHandler(address='/dev/log')
        handler.setFormatter(self.formatter)
        handler.set_name(handlername)

        if level == 1:
            handler.setLevel(logging.DEBUG)
        if level == 2:
            handler.setLevel(logging.INFO)
        if level == 3:
            handler.setLevel(logging.WARNING)
        if level == 4:
            handler.setLevel(logging.ERROR)
        if level == 5:
            handler.setLevel(logging.CRITICAL)

        logger.addHandler(handler)
        return logger
