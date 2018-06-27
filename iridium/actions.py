import logging
from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def wait_element_located(driver, xpath, wait=10):
    element = WebDriverWait(driver, wait).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script('arguments[0].scrollIntoView(behavior="smooth");', element)
    return element


def wait_element_clickable(driver, xpath, wait=10):
    element = WebDriverWait(driver, wait).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script('arguments[0].scrollIntoView(behavior="smooth");', element)
    return element


def wait_until_condition(driver, condition, wait=10):
    element = WebDriverWait(driver, wait).until(condition)
    driver.execute_script('arguments[0].scrollIntoView(behavior="smooth");', element)
    return element


# def random_sleep(min_sleep=0.6, max_sleep=1):
#     sleep(random.uniform(min_sleep, max_sleep))


class BrowserAction:
    """ Abstract """

    logger = logging.getLogger('Iridium')

    def execute(self, driver: WebDriver):
        raise NotImplementedError


class OpenPage(BrowserAction):

    def __init__(self, url: str):
        self.url = url
        # self.timeout = timeout  TODO

    def execute(self, driver: WebDriver):
        self.logger.debug('[OpenPage] %s', self.url)
        driver.get(self.url)


class Exists(BrowserAction):

    def __init__(self, xpath, timeout=10):
        self.xpath = xpath
        self.timeout = timeout

    def execute(self, driver: WebDriver) -> bool:
        try:
            wait_element_clickable(driver, xpath=self.xpath, wait=self.timeout)
        except (NoSuchElementException, TimeoutException):
            self.logger.debug('[Exists] Fale XPATH: %s', self.xpath)
            return False
        else:
            self.logger.debug('[Exists] True XPATH: %s', self.xpath)
            return True


class Click(BrowserAction):

    def __init__(self, xpath, timeout=60):
        self.xpath = xpath
        self.timeout = timeout

    def execute(self, driver: WebDriver) -> None:
        wait_element_clickable(driver, xpath=self.xpath, wait=self.timeout).click()
        self.logger.debug('[Click] XPATH: %s', self.xpath)


class Input(BrowserAction):

    def __init__(self, text: str, xpath, timeout=60):
        self.xpath = xpath
        self.text = text
        self.timeout = timeout

    def execute(self, driver: WebDriver):
        wait_element_located(driver, xpath=self.xpath, wait=self.timeout).clear()
        wait_element_located(driver, xpath=self.xpath, wait=self.timeout).send_keys(self.text)
        self.logger.debug('[Input] "%s" XPATH: %s', self.text, self.xpath)


class Read(BrowserAction):

    def __init__(self, xpath, timeout=60):
        self.xpath = xpath
        self.timeout = timeout

    def execute(self, driver: WebDriver) -> str:
        text = wait_element_located(driver, self.xpath, self.timeout).text
        self.logger.debug('[Read] "%s" XPATH: %s', text, self.xpath)
        return text


class RaiseOnExist(BrowserAction):

    def __init__(self, xpath, timeout=5, exception=None):
        self.xpath = xpath
        self.timeout = timeout
        self.exception = exception

    def execute(self, driver: WebDriver) -> None:
        try:
            wait_element_located(driver, self.xpath, self.timeout)
            raise self.exception or Exception('Element found: %s' % self.xpath)
        except (NoSuchElementException, TimeoutException):
            self.logger.debug('[RaiseOnExist] ok. XPATH: %s', self.xpath)


class Sleep(BrowserAction):

    def __init__(self, sleep_time: int):
        self.sleep_time = sleep_time

    def execute(self, driver: WebDriver) -> None:
        self.logger.debug('[Sleep] Starting sleep %s seconds ...', self.sleep_time)
        sleep(self.sleep_time)


class MakeScreen(BrowserAction):

    def __init__(self, file_name='screen.png'):
        self.file_name = file_name

    def execute(self, driver: WebDriver) -> None:
        driver.save_screenshot(self.file_name)
        self.logger.debug('[MakeScreen] %s', self.file_name)
