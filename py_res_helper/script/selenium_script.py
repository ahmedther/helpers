import multiprocessing
import os
import shutil

# import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from enum import Enum, unique
from time import sleep

profile_path = os.path.join(
    os.getenv("APPDATA"),
    "Mozilla",
    "Firefox",
    "Profiles",
    "a2mb7obs.default",
)

auto_path = os.path.join(
    os.getenv("APPDATA"),
    "Mozilla",
    "Firefox",
    "Profiles",
    "automate",
)


@unique
class AIList(Enum):
    GEMINI = "gemini"
    CHATGPT = "chatgpt"
    META_AI = "meta.ai"
    COPILOT = "copilot"


class FirefoxBrowser:
    def __init__(self, ai_to_run):
        # self.search = search

        firefox_profile = webdriver.FirefoxProfile(auto_path)
        firefox_options = webdriver.FirefoxOptions()

        firefox_options.profile = firefox_profile  # Set the existing profile

        firefox_options.add_argument("--private")

        firefox_service = webdriver.firefox.service.Service(
            GeckoDriverManager().install()
        )

        self.driver = webdriver.Firefox(
            service=firefox_service, options=firefox_options
        )
        self.actions = ActionChains(self.driver)

        self.driver.implicitly_wait(5)
        self.reset_zoom()

        self.ai_to_run_driver(ai_to_run)

    def ai_to_run_driver(self, ai_to_run):
        match ai_to_run:
            case "gemini":
                return self.tab_gemini()
            case "chatgpt":
                return self.tab_chatgpt()
            case "meta.ai":
                return self.tab_meta_ai()
            case _:
                return self.tab_copilot()

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

    def perform_search_action(self, element: WebElement):
        element.click()
        self.actions.key_down(Keys.CONTROL).send_keys("v").key_up(
            Keys.CONTROL
        ).send_keys(Keys.ENTER).perform()

    def tab_gemini(self):
        self.driver.get("https://gemini.google.com/")
        text_area = self.driver.find_element(By.CLASS_NAME, "ql-editor")
        sleep(1)
        self.perform_search_action(text_area)
        # text_area.send_keys(self.search, Keys.ENTER)

    def tab_chatgpt(self):
        self.driver.get("https://chatgpt.com/?model=gpt-4o")
        text_area = self.driver.find_element(By.ID, "prompt-textarea")
        self.perform_search_action(text_area)
        # text_area.send_keys(self.search, Keys.ENTER)

    def tab_meta_ai(self):
        self.driver.get("https://www.meta.ai/")
        # text_area = self.driver.find_element(By.ID, ":r6:")
        text_area = self.driver.find_element(
            By.XPATH, "//textarea[@placeholder='Ask Meta AI anything...']"
        )
        self.perform_search_action(text_area)

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
        self.perform_search_action(text_area)

        # text_area.send_keys(self.search, Keys.ENTER)


# Standalone Function (Not part of the Firefox Browser Class)
def copy_cookies_db() -> str:

    # Create the destination directory if it doesn't exist
    if not os.path.exists(auto_path):
        os.makedirs(auto_path)

    # Source file path
    src_file = os.path.join(profile_path, "cookies.sqlite")

    # Destination file path
    dest_file = os.path.join(auto_path, "cookies.sqlite")

    if os.path.exists(dest_file):
        os.remove(dest_file)

    # Copy the file
    shutil.copy2(src_file, dest_file)


if __name__ == "__main__":
    # search_query = pyperclip.paste()
    copy_cookies_db()
    pool = multiprocessing.Pool(processes=1)
    # pool.apply_async(FirefoxBrowser, args=(search_query, "gemini"))
    # pool.apply_async(FirefoxBrowser, args=(search_query, "co-pilot"))
    pool.apply_async(FirefoxBrowser, args=(AIList.GEMINI.value,))
    # pool.apply_async(FirefoxBrowser, args=(AIList.COPILOT.value,))
    # pool.apply_async(FirefoxBrowser, args=(AIList.CHATGPT.value,))
    # pool.apply_async(FirefoxBrowser, args=(AIList.META_AI.value,))
    pool.close()
    pool.join()
    # FirefoxBrowser(ai_to_run=AIList.CHATGPT.value,)
