
1. **Create a new Firefox profile**:

   - Open a command prompt or terminal.
   - Navigate to your Firefox installation directory (e.g., `C:\Program Files\Mozilla Firefox` on Windows).
   - Run the following command to create a new profile:

     ```
     firefox.exe -no-remote -CreateProfile "AutomationProfile"
     ```

     Replace `"AutomationProfile"` with the desired name for your new profile.

2. **Copy the necessary data from your existing profile to the new profile**:

   - Open Firefox with your existing profile.
   - Navigate to `about:profiles` in the address bar.
   - Find the path to your existing profile (e.g., `C:\Users\YourUsername\AppData\Roaming\Mozilla\Firefox\Profiles\<your_existing_profile>`).
   - Close Firefox.
   - Copy the `cookies.sqlite` file from your existing profile to the new profile's directory (e.g., `C:\Users\YourUsername\AppData\Roaming\Mozilla\Firefox\Profiles\AutomationProfile`).

3. **Modify your script to use the new profile**:

   ```python
   import os
   from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

   def __init__(self, search, ai_to_run):
       self.search = search

       # Path to your new Firefox profile
       profile_path = os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles", "AutomationProfile")

       firefox_profile = FirefoxProfile(profile_path)
       firefox_options = webdriver.FirefoxOptions()
       firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
       firefox_options.profile = firefox_profile  # Set the new profile

       # firefox_options.add_argument("--private")

       firefox_service = webdriver.firefox.service.Service(
           GeckoDriverManager().install()
       )
       self.driver = webdriver.Firefox(
           service=firefox_service, options=firefox_options
       )

       self.driver.implicitly_wait(5)
       self.reset_zoom()
   ```

   Replace `"AutomationProfile"` with the name you chose for your new profile.

By creating a new Firefox profile and copying only the necessary data (in this case, the `cookies.sqlite` file), you can significantly reduce the time it takes for Selenium to launch the browser with your automation script.

Additionally, you can consider using a lightweight Firefox profile manager tool like `ProfileMaker` to create and manage separate profiles for different purposes, including automation.