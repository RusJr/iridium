import logging.config
import os
import platform
from logging import FileHandler
from logging.handlers import RotatingFileHandler
from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from iridium.actions import BrowserAction


class ChromeBrowser:
    """
    Default browser Chrome
    Find browser path on Ubuntu: 'which firefox'
    """

    _chromedriver_map = {
        'Linux': '/_webdriwers/linux64_chromedriver',
        'Windows': '/_webdriwers/win32_chromedriver.exe',
        'Darwin': '/_webdriwers/mac64_chromedriver',
    }

    # accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    window_size = (1366, 768)
    page_load_timeout = 15

    def __init__(self, logging_file=None, headless=False):
        self.logger = logging.getLogger('Iridium')
        self._init_logging(logging_file)
        self.browser = None
        self._open_browser(headless)

    def __del__(self):
        self._close_browser()

    def execute(self, actions: List[BrowserAction], delay=0):
        for number, action in enumerate(actions, 1):
            try:
                action.execute(self.browser)
            except Exception as e:
                self.logger.error('[%s] Error on command %s: %s', type(action).__name__, number, e)
                raise e
            sleep(delay)
        self.logger.info('Script executed')

    @property
    def _chromedriver_path(self) -> str:
        abs_dir_path = os.path.join(os.path.dirname(__file__))
        platform_name = platform.system()
        try:
            return abs_dir_path + self._chromedriver_map[platform_name]
        except KeyError:
            raise Exception('OS detecting problem (%s)' % platform_name)

    def _open_browser(self, headless=False):

        options = Options()
        options.headless = headless

        self.browser = webdriver.Chrome(self._chromedriver_path, chrome_options=options)
        self.browser.set_window_size(*self.window_size)
        self.browser.delete_all_cookies()
        self.browser.set_page_load_timeout(self.page_load_timeout)
        self.logger.debug('Started browser instance')

    def _close_browser(self):
        if hasattr(self, 'browser') and self.browser:
            self.browser.quit()
        # self.logger.debug('browser closed')

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
                                               # 'maxBytes': 10485760}
            log_dict['loggers']['Iridium']['handlers'].append('ir_file')

        logging.config.dictConfig(log_dict)