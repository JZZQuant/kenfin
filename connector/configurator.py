from kiteconnect import KiteConnect
import time
import argparse
from connector.auth_stack import AuthSingletonStack
from connector.driver import Driver


class Configurator(object):
    def __init__(self, driver_path=None):
        # lazy evaluate the driver inside the get_config and kill it by the end

        driver = Driver()
        with driver as d:
            single_auth = AuthSingletonStack().pop()
            self.api_key = single_auth["api_key"]
            self.secret_key = single_auth["secret_key"]
            self.u_id = single_auth["u_id"]
            self.password = single_auth["password"]
            self.kite = KiteConnect(self.api_key, self.secret_key)

            # Hit the first url and get session_id
            d.get(self.kite.login_url())
            self.session_id = driver.parse_url("sess_id")

            # login to first auth page
            user_id = d.find_elements_by_tag_name("input")[0]
            pwd = d.find_elements_by_tag_name("input")[1]
            login = d.find_element_by_xpath('//button[@type="submit"]')
            user_id.send_keys(self.u_id)
            pwd.send_keys(self.password)
            login.click()

            # Wait for second auth page to load and fill the second factor authentication question
            time.sleep(15)
            driver.fill_second_factor_auth_question(0)
            driver.fill_second_factor_auth_question(1)
            login.click()

            # return request token from final url
            self.request_token = driver.parse_url("request_token")
            self.data = self.kite.generate_session(api_secret=self.secret_key, request_token=self.request_token)
            self.access_token = self.data["access_token"]
            self.public_token = self.data["public_token"]
            self.user_id = self.data["user_id"]
            self.nfo = self.kite.instruments("NFO")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--driver_path", help="Custom path to the chrome driver for headless running",
                        default=None)
    args = parser.parse_args()
    config = Configurator(args.driver_path)
    print(
        "current login : \n \t session id: %s \n "
        " \t request token: %s \n \t access_token: %s \n"
        " \t public_token: %s \n \t user_id: %s" %
        (config.session_id, config.request_token, config.access_token, config.public_token, config.user_id)
    )
