import logging as _log
import serial as _serial
import os
from PyQt5.QtCore import QThread , pyqtSignal

class Log:
    def __init__(self, target: str = 'main') -> None:

        if not os.path.exists("log/"):
            os.mkdir("log/")

        self.logger = _log
        self.logger.basicConfig(format='[%(levelname)s] In %(name)s - %(asctime)s - %(message)s',
                                datefmt='%d-%b-%y %H:%M:%S',
                                level=self.logger.INFO,
                                handlers=[
                                    self.logger.FileHandler('log/log.log', mode='a', encoding='utf-8'),
                                    self.logger.StreamHandler()
                                ]
                                )
        self.target = '[' + target.upper() + '] '

    def debug(self, msg, *args, **kwargs) -> None:
        self.logger.debug(self.target + msg, *args, **kwargs)
        return

    def info(self, msg, *args, **kwargs) -> None:
        self.logger.info(self.target + msg, *args, **kwargs)
        return

    def warn(self, msg, *args, **kwargs) -> None:
        self.logger.warning(self.target + msg, *args, **kwargs)
        return

    def error(self, msg, *args, **kwargs) -> None:
        self.logger.error(self.target + msg, *args, **kwargs)
        return

    def critical(self, msg, *args, **kwargs) -> None:
        self.logger.critical(self.target + msg, *args, **kwargs)
        return

    def exception(self, msg, *args, **kwargs) -> None:
        self.logger.exception(self.target + msg, *args, **kwargs)
        return

class LogSerial:
    def __init__(self, device: _serial.Serial, /, *, header) -> None:
        """
        Serial Logger object class
        :param device:
        :param header:
        """
        self.device = device
        self.header = header
        self.raw = ''
        self.payload = ''
        self.buffer = ''
        self._is_updated = False
        self._find1 = 0
        self._find2 = 0
        self.logger = Log()
        self.read_result = True

class ThreadSerial(QThread):
    msg_carrier = Signal(object)

    def __init__(self, *args, parent=None, serial_logger, **kwargs) -> None:
        super(ThreadSerial, self).__init__(parent)
        self.serial_logger = serial_logger
        self.args = args
        self.kwargs = kwargs
        self.logger = Log('LOG_THREAD')
        self._isRunning = True

    def __del__(self) -> None:
        try:
            self.wait()
            self.logger.info('Serial thread deleted successfully.')
        except RuntimeError:
            self.logger.exception('Unable to delete the serial thread.')
            pass
        return

    def run(self) -> None:
        self.logger.info('Starting the serial thread.')
        try:
            self.serial_logger.readPayload(_ilib.wrapper(self.update_msg))
        except Exception:
            return
        return

    def stop(self) -> None:
        self.logger.info('Try stopping the serial thread.')
        self._isRunning = False
        self.terminate()
        self.logger.info('Stopped the serial thread.')
        return

    def update_msg(self, str_out) -> None:
        self.logger.debug('Emitted ' + str(str_out))
        self.msg_carrier.emit(str_out)
        return