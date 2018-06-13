import logging.config
import os
import platform
from time import sleep
from typing import List

from selenium import webdriver

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

    def __init__(self):
        self.browser = None
        self.logger = logging.getLogger('Iridium')
        self._open_browser()

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

    def _open_browser(self):
        self.browser = webdriver.Chrome(self._chromedriver_path)
        self.browser.set_window_size(*self.window_size)
        # self.browser.delete_all_cookies()
        self.browser.set_page_load_timeout(self.page_load_timeout)
        self.logger.debug('Started browser instance')

    def _close_browser(self):
        if self.browser:
            self.browser.quit()
        self.logger.debug('browser closed')
