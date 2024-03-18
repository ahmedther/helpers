import multiprocessing
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


class FirefoxBrowser:
    def __init__(self, search, ai_to_run):
        self.search = search
        profile_path = os.path.join(
            os.getenv("APPDATA"),
            "Mozilla",
            "Firefox",
            "Profiles",
            "atex6pqj.default-release",
        )

        firefox_profile = webdriver.FirefoxProfile(profile_path)
        firefox_options = webdriver.FirefoxOptions()

        firefox_options.profile = firefox_profile  # Set the existing profile

        firefox_options.add_argument("--private")

        firefox_service = webdriver.firefox.service.Service(
            GeckoDriverManager().install()
        )

        self.driver = webdriver.Firefox(
            service=firefox_service, options=firefox_options
        )

        self.driver.implicitly_wait(5)
        self.reset_zoom()
        if ai_to_run == "gemini":
            self.tab_gemini()
        else:
            self.search = self.search[:4000]
            self.tab_copilot()

    def reset_zoom(self):
        "Sets zoom level to 100%"
        self.driver.execute_script("document.body.style.zoom='90%'")

    def find_shadow_root(self, host_element):
        return self.driver.execute_script(
            "return arguments[0].shadowRoot", host_element
        )

    def close_browser(self):
        """
        Closes the currently opened browser.
        """
        self.driver.quit()

    def open_new_tab(self):
        # Open a new tab
        self.driver.execute_script("window.open('');")
        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def tab_gemini(self):
        self.driver.get("https://gemini.google.com/")
        text_area = self.driver.find_element(By.CLASS_NAME, "ql-editor")
        text_area.send_keys(self.search, Keys.ENTER)

    def tab_copilot(self):
        self.driver.get("https://copilot.microsoft.com/")
        shadow_root_1 = self.find_shadow_root(
            self.driver.find_element(By.TAG_NAME, "cib-serp")
        )
        shadow_root_2 = self.find_shadow_root(
            shadow_root_1.find_element(By.ID, "cib-conversation-main")
        )
        shadow_root_3 = self.find_shadow_root(
            shadow_root_2.find_element(
                By.CSS_SELECTOR,
                "cib-welcome-container[product='bing'][chat-type='consumer']",
            )
        )
        shadow_root_4 = self.find_shadow_root(
            shadow_root_3.find_element(
                By.CSS_SELECTOR,
                "cib-tone-selector[visible][product='bing'][chat-type='consumer'][goldilocks-stroke]",
            )
        )

        button = shadow_root_4.find_element(
            By.CSS_SELECTOR, 'button.tone-precise[role="radio"]'
        )
        button.click()

        text_shadow_root_1 = self.find_shadow_root(
            shadow_root_1.find_element(
                By.CSS_SELECTOR, "cib-action-bar#cib-action-bar-main"
            )
        )
        text_shadow_root_2 = self.find_shadow_root(
            text_shadow_root_1.find_element(By.CSS_SELECTOR, "cib-text-input")
        )

        text_area = text_shadow_root_2.find_element(
            By.CSS_SELECTOR, "textarea#searchbox"
        )
        text_area.send_keys(self.search, Keys.ENTER)


if __name__ == "__main__":
    search_query = "Gemini is the best AI?"
    pool = multiprocessing.Pool(processes=2)
    pool.apply_async(FirefoxBrowser, args=(search_query, "gemini"))
    pool.apply_async(FirefoxBrowser, args=(search_query, "co-pilot"))
    pool.close()
    pool.join()


# class BaseBrowser:
#     def __init__(self):
#         self.driver.implicitly_wait(5)
#         self.reset_zoom()

#     def reset_zoom(self):
#         "Sets zoom level to 100%"
#         self.driver.execute_script("document.body.style.zoom='100%'")

#     def find_shadow_root(self, host_element):
#         return self.driver.execute_script(
#             "return arguments[0].shadowRoot", host_element
#         )

#     def close_browser(self):
#         self.driver.quit()

#     def open_new_tab(self):
#         # Open a new tab
#         self.driver.execute_script("window.open('');")
#         # Switch to the new tab
#         self.driver.switch_to.window(self.window_handles[-1])

#     def close_browser(self):
#         self.driver.quit()


# class LaunchChrome(BaseBrowser):
#     def __init__(self, search):
#         self.search = search

#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument("--enable-chrome-browser-cloud-management")
#         chrome_options.add_argument(
#             r"--user-data-dir=C:\Users\AHMED\AppData\Local\Google\Chrome\User Data"
#         )

#         chrome_service = webdriver.chrome.service.Service(
#             ChromeDriverManager().install()
#         )
#         self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#         super().__init__()

#         self.tab_gemini()

#         # self.open_new_tab()

#     def tab_gemini(self):
#         self.driver.get("https://gemini.google.com/")

#         text_area = self.driver.find_element(By.CLASS_NAME, "ql-editor")
#         text_area.send_keys(self.search, Keys.ENTER)


# class LaunchFireFox(BaseBrowser):
#     def __init__(self, search):
#         self.search = search

#         firefox_options = webdriver.FirefoxOptions()
#         firefox_options.add_argument("--private")

#         firefox_service = webdriver.firefox.service.Service(
#             GeckoDriverManager().install()
#         )
#         self.driver = webdriver.Firefox(
#             service=firefox_service, options=firefox_options
#         )

#         super().__init__()

#         self.tab_copilot()

#     def tab_copilot(self):
#         self.driver.get("https://copilot.microsoft.com/")

#         shadow_root_1 = self.find_shadow_root(
#             self.driver.find_element(By.TAG_NAME, "cib-serp")
#         )
#         shadow_root_2 = self.find_shadow_root(
#             shadow_root_1.find_element(By.ID, "cib-conversation-main")
#         )
#         shadow_root_3 = self.find_shadow_root(
#             shadow_root_2.find_element(
#                 By.CSS_SELECTOR,
#                 "cib-welcome-container[product='bing'][chat-type='consumer']",
#             )
#         )
#         shadow_root_4 = self.find_shadow_root(
#             shadow_root_3.find_element(
#                 By.CSS_SELECTOR,
#                 "cib-tone-selector[visible][product='bing'][chat-type='consumer'][goldilocks-stroke]",
#             )
#         )

#         button = shadow_root_4.find_element(
#             By.CSS_SELECTOR, 'button.tone-precise[role="radio"]'
#         )
#         button.click()

#         text_shadow_root_1 = self.find_shadow_root(
#             shadow_root_1.find_element(
#                 By.CSS_SELECTOR, "cib-action-bar#cib-action-bar-main"
#             )
#         )
#         text_shadow_root_2 = self.find_shadow_root(
#             text_shadow_root_1.find_element(By.CSS_SELECTOR, "cib-text-input")
#         )

#         text_area = text_shadow_root_2.find_element(
#             By.CSS_SELECTOR, "textarea#searchbox"
#         )
#         text_area.send_keys(self.search, Keys.ENTER)


# def tab_copilot(self):
#     # Navigate to www.google.com
#     self.get("https://copilot.microsoft.com/")

#     host_element_shadow_1 = self.driver.find_element(By.TAG_NAME, "cib-serp")
#     shadow_root_1 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_1)

#     # # Find the element containing the next shadow root inside the first shadow root
#     host_element_shadow_2 = shadow_root_1.find_element(By.ID, "cib-conversation-main")
#     shadow_root_2 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_2)

#     # Finidng the More Precise button
#     host_element_shadow_3 = shadow_root_2.find_element(By.CSS_SELECTOR, "cib-welcome-container[product='bing'][chat-type='consumer']")
#     shadow_root_3 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_3)

#     host_element_shadow_4 = shadow_root_3.find_element(By.CSS_SELECTOR, "cib-tone-selector[visible][product='bing'][chat-type='consumer'][goldilocks-stroke]")
#     shadow_root_4 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_4)
#     button = shadow_root_4.find_element(By.CSS_SELECTOR, 'button.tone-precise[role="radio"]')
#     button.click()

# #Finding Text Box
# host_text_shadow_1 = shadow_root_1.find_element(By.CSS_SELECTOR, "cib-action-bar#cib-action-bar-main")
# text_shadow_root_1 = self.execute_script("return arguments[0].shadowRoot", host_text_shadow_1)

# host_text_shadow_2 = text_shadow_root_1.find_element(By.CSS_SELECTOR, 'cib-text-input')
# text_shadow_root_2 = self.execute_script("return arguments[0].shadowRoot", host_text_shadow_2)

# text_area = text_shadow_root_2.find_element(By.CSS_SELECTOR, 'textarea#searchbox')
# text_area.send_keys(self.search,Keys.ENTER)
