from selenium import webdriver
import selenium as se
import urllib.parse as urlparse
import time

from logger.heirarchical_logger import info


class Driver():
    def __init__(self, driver_path=None):
        self.options = se.webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver_path = driver_path

    def __enter__(self):
        if self.driver_path is None:
            self.__driver__ = se.webdriver.Chrome(chrome_options=self.options)
        else:
            self.__driver__ = se.webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.options)
        return self.__driver__

    def __exit__(self, type, value, traceback):
        self.__driver__.quit()

    def parse_url(self, key):
        time.sleep(60)
        session_url = self.__driver__.current_url
        info("current url : %s " % str(session_url))
        parsed = urlparse.urlparse(session_url)
        value = urlparse.parse_qs(parsed.query)[key][0]
        return value

    def fill_second_factor_auth_question(self, index):
        question = self.__driver__.find_elements_by_tag_name('label')[index].text.lower()
        answer = self.__driver__.find_elements_by_tag_name('input')[index]
        ans = ""
        if "graduation" in question:
            ans = "2006"
        if "mobile" in question:
            ans = "apple"
        if "tv" in question:
            ans = "lg"
        if "insurance" in question:
            ans = "sbi"
        if "bank" in question:
            ans = "icici"
        answer.send_keys(ans)
