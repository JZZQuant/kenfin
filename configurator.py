from kiteconnect import KiteConnect
from selenium import webdriver
import selenium as se
import time
import urllib.parse as urlparse
import argparse

api_key = "zka582z590jag8yh"
secret_key = "9zdlmklim6rsakd2fkhay59hybsm5mw6"
u_id = "RD0291"
password = "Divakar@1983"


class Configurator(object):
    def __init__(self, driver_path=None):
        # look for the readme file to get automated headless chromedrive
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        if driver_path is None:
            self.driver = se.webdriver.Chrome(chrome_options=options)
        else:
            self.driver = se.webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    def fill_second_factor_auth_question(self, index):
        question = self.driver.find_elements_by_tag_name('label')[index].text.lower()
        answer = self.driver.find_elements_by_tag_name('input')[index]
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

    def get_config(self):
        kite = KiteConnect(api_key, secret_key)
        url = kite.login_url()

        # Hit the first url and get session_id
        self.driver.get(url)
        self.session_id = self.parse_url("sess_id")

        # login to first auth page
        user_id = self.driver.find_elements_by_tag_name("input")[0]
        pwd = self.driver.find_elements_by_tag_name("input")[1]
        login = self.driver.find_element_by_xpath('//button[@type="submit"]')
        user_id.send_keys(u_id)
        pwd.send_keys(password)
        login.click()

        # Wait for second auth page to load and fill the second factor authentication question
        time.sleep(15)
        self.fill_second_factor_auth_question(0)
        self.fill_second_factor_auth_question(1)
        login.click()

        # return request token from final url
        self.request_token = self.parse_url("request_token")

        self.data = kite.generate_session(api_secret=secret_key, request_token=self.request_token)
        self.access_token = self.data["access_token"]

    def parse_url(self, key):
        time.sleep(20)
        session_url = self.driver.current_url
        parsed = urlparse.urlparse(session_url)
        value = urlparse.parse_qs(parsed.query)[key][0]
        return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--driver_path", help="Custom path to the chrome driver for headless running",
                        default=None)
    args = parser.parse_args()
    config = Configurator(args.driver_path)
    config.get_config()
    print("current login : \n \t session id: %s \n  \t request token: %s \n \t access_token: %s " % (
        config.session_id, config.request_token, config.access_token))
