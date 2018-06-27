import logging.config
import os
import platform
import socket
from http.client import CannotSendRequest
from logging import FileHandler
from logging.handlers import RotatingFileHandler
from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command

from iridium.actions import BrowserAction


class ChromeBrowser:
    """
    finds Chrome automatically
    """

    window_size = (1366, 768)
    page_load_timeout = 60

    _chromedriver_map = {
        'Linux': '/_webdriwers/linux64_chromedriver',
        'Windows': '/_webdriwers/win32_chromedriver.exe',
        'Darwin': '/_webdriwers/mac64_chromedriver',
    }

    def __init__(self, logging_file=None, headless=False):
        self.logger = logging.getLogger('Iridium')
        self._init_logging(logging_file)
        # self.action_timeout = action_timeout
        self.browser = None
        self.open_browser(headless)

    def __del__(self):
        self.close_browser()

    def open_browser(self, headless=False):
        if not self.browser_is_open:
            options = Options()
            options.headless = headless

            self.browser = webdriver.Chrome(self._chromedriver_path, chrome_options=options)
            self.browser.set_window_size(*self.window_size)
            self.browser.delete_all_cookies()
            self.browser.set_page_load_timeout(self.page_load_timeout)
            self.logger.debug('Started browser instance')
        else:
            self.logger.debug('Browser already open')

    @property
    def browser_is_open(self) -> bool:
        if hasattr(self, 'browser') and self.browser:
            try:
                status = self.browser.execute(Command.STATUS)
                return True
            except (socket.error, CannotSendRequest):
                pass
        return False

    def close_browser(self):
        if self.browser_is_open:
            try:
                self.browser.quit()
            except ImportError:
                pass

    def execute(self, actions: List[BrowserAction], delay=0):
        for number, action in enumerate(actions, 1):
            try:
                action.execute(self.browser)
            except Exception as e:
                self.logger.error('[%s] Error on command %s: %s', type(action).__name__, number, e)
                raise e
            sleep(delay)
        self.logger.info('Script executed')

    def run(self, action: BrowserAction):
        return action.execute(self.browser)

    @property
    def _chromedriver_path(self) -> str:
        abs_dir_path = os.path.join(os.path.dirname(__file__))
        platform_name = platform.system()
        try:
            return abs_dir_path + self._chromedriver_map[platform_name]
        except KeyError:
            raise Exception('OS detecting problem (%s)' % platform_name)

    def _init_logging(self, logging_file=None):
        log_dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {'ir_format': {'format': '[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s',
                                         'datefmt': '%d/%m/%Y %H:%M:%S'}},
            'handlers': {'ir_console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'ir_format'}},
            'loggers': {'Iridium': {'handlers': ['ir_console'], 'propagate': False, 'level': 'DEBUG'}, }
        }

        if logging_file:
            log_dict['handlers']['ir_file'] = {'class': 'logging.handlers.RotatingFileHandler',
                                               'filename': logging_file,
                                               'mode': 'w',
                                               'formatter': 'ir_format', }
            log_dict['loggers']['Iridium']['handlers'].append('ir_file')

        logging.config.dictConfig(log_dict)