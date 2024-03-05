import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LaunchBrowser(webdriver.Chrome):
    def __init__(self,search):
        self.search = search
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-chrome-browser-cloud-management")
        chrome_options.add_argument(r"--user-data-dir=C:\Users\AHMED\AppData\Local\Google\Chrome\User Data")

        self.driverpath =  os.path.join(os.getcwd(), "chromedriver.exe")


        os.environ ['PATH'] = self.driverpath
        super(LaunchBrowser, self).__init__(options=chrome_options)

        self.implicitly_wait(5)

        self.launch_browser()
        
        self.first_tab_gemini()

        self.open_new_tab()

        self.second_tab_copilot()
        
        inpu2t= input("wait")


    def launch_browser(self):
        self.get("https://gemini.google.com/")

    def first_tab_gemini(self):
        text_area = self.find_element(By.CLASS_NAME,'ql-editor')
        text_area.send_keys(self.search,Keys.ENTER)

    def open_new_tab(self):
        # Open a new tab
        self.execute_script("window.open('');")
        # Switch to the new tab
        self.switch_to.window(self.window_handles[-1])

        
    def second_tab_copilot(self):
        # Navigate to www.google.com
        self.get("https://copilot.microsoft.com/")
        
        host_element_shadow_1 = self.find_element(By.TAG_NAME, "cib-serp")
        shadow_root_1 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_1)
        
        # # Find the element containing the next shadow root inside the first shadow root
        host_element_shadow_2 = shadow_root_1.find_element(By.ID, "cib-conversation-main")
        shadow_root_2 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_2)
        
        # Finidng the More Precise button
        host_element_shadow_3 = shadow_root_2.find_element(By.CSS_SELECTOR, "cib-welcome-container[product='bing'][chat-type='consumer']") 
        shadow_root_3 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_3)
        
        host_element_shadow_4 = shadow_root_3.find_element(By.CSS_SELECTOR, "cib-tone-selector[visible][product='bing'][chat-type='consumer'][goldilocks-stroke]")
        shadow_root_4 = self.execute_script("return arguments[0].shadowRoot", host_element_shadow_4)

        button = shadow_root_4.find_element(By.CSS_SELECTOR, 'button.tone-precise[role="radio"]')
        button.click()

        #Finding Text Box
        host_text_shadow_1 = shadow_root_1.find_element(By.CSS_SELECTOR, "cib-action-bar#cib-action-bar-main")
        text_shadow_root_1 = self.execute_script("return arguments[0].shadowRoot", host_text_shadow_1)

        host_text_shadow_2 = text_shadow_root_1.find_element(By.CSS_SELECTOR, 'cib-text-input')
        text_shadow_root_2 = self.execute_script("return arguments[0].shadowRoot", host_text_shadow_2)

        text_area = text_shadow_root_2.find_element(By.CSS_SELECTOR, 'textarea#searchbox')
        text_area.send_keys(self.search,Keys.ENTER)

        print(text_area)








if __name__ == "__main__":
    LaunchBrowser("What is Gemini") 

