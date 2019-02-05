from kiteconnect import KiteConnect
from selenium import webdriver
import selenium as se
import time
import urllib.parse as urlparse
import argparse

from connector.auth_stack import AuthStack


class Configurator(object):
    def __init__(self, driver_path=None):
        # look for the readme file to get automated headless chromedrive
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        if driver_path is None:
            self.driver = se.webdriver.Chrome(chrome_options=options)
        else:
            self.driver = se.webdriver.Chrome(executable_path=driver_path, chrome_options=options)

        single_auth = AuthStack()
        self.api_key = single_auth.api_key
        self.secret_key = single_auth.secret_key
        self.u_id = single_auth.u_id
        self.password = single_auth.password

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
        kite = KiteConnect(self.api_key, self.secret_key)
        url = kite.login_url()

        # Hit the first url and get session_id
        self.driver.get(url)
        self.session_id = self.parse_url("sess_id")

        # login to first auth page
        user_id = self.driver.find_elements_by_tag_name("input")[0]
        pwd = self.driver.find_elements_by_tag_name("input")[1]
        login = self.driver.find_element_by_xpath('//button[@type="submit"]')
        user_id.send_keys(self.u_id)
        pwd.send_keys(self.password)
        login.click()

        # Wait for second auth page to load and fill the second factor authentication question
        time.sleep(15)
        self.fill_second_factor_auth_question(0)
        self.fill_second_factor_auth_question(1)
        login.click()

        # return request token from final url
        self.request_token = self.parse_url("request_token")

        self.data = kite.generate_session(api_secret=self.secret_key, request_token=self.request_token)
        self.access_token = self.data["access_token"]
        self.public_token = self.data["public_token"]
        self.user_id = self.data["user_id"]
        self.kite=kite
        self.driver.quit()

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
    print(
        "current login : \n \t session id: %s \n  \t request token: %s \n \t access_token: %s \n \t public_token: %s \n \t user_id: %s" % (
            config.session_id, config.request_token, config.access_token, config.public_token, config.user_id))
