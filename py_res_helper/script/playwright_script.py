import asyncio
import os
import shutil
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from enum import Enum, unique


@unique
class AIList(Enum):
    GEMINI = "gemini"
    CHATGPT = "chatgpt"
    META_AI = "meta.ai"
    COPILOT = "copilot"


class PlaywrightHelper:
    def __init__(self, data_dir="User Data"):

        self.chromium_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Chromium")

        self.user_data_dir = os.path.join(self.chromium_dir, data_dir)

        if data_dir != "User Data":
            self.user_data_dir = os.path.join(self.chromium_dir, f"User Data{data_dir}")

            self.copy_chromium_user_data(
                os.path.join(self.chromium_dir, "User Data"), self.user_data_dir
            )

        self.ua = UserAgent()

    def copy_chromium_user_data(self, src_dir, dst_dir):

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

            for item in os.listdir(src_dir):
                src_item = os.path.join(src_dir, item)
                dst_item = os.path.join(dst_dir, item)

                if os.path.isfile(src_item):
                    shutil.copy2(src_item, dst_item)
                else:
                    shutil.copytree(src_item, dst_item)

            print(f"Folder '{dst_dir}' created and populated.")
            return True
        else:
            print(f"Folder '{dst_dir}' already exists.")
            return False

    async def launch_browser(self):

        self.playwright = await async_playwright().start()
        os.environ["CHROME_AUTOMATION_DISABLED"] = "1"

        self.browser = await self.playwright.chromium.launch_persistent_context(
            headless=False,  # Required for stealth mode
            user_data_dir=self.user_data_dir,
            args=[
                "--disable-web-security",
                "--disable-plugin-discovery",
                "--disable-browser-notification",
                "--disable-logging",
                "--disable-automation",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=Out-of-blink-cursors",
                "--disable-features=ChromeInfobars",
                "--disable-infobars"
                # "--incognito",
                "--no-first-run",
                "--no-sandbox",
                "--mute-audio",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--no-zygote",
                # "--single-process",
                "--no-automation",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-extensions",
                "--disable-popup-blocking",
                "--disable-translate",
                "--disable-sync",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-breakpad",
                "--disable-client-side-phishing-detection",
                "--disable-component-extensions-with-background-pages",
                "--disable-default-apps",
                "--disable-features=TranslateUI",
                "--disable-hang-monitor",
                "--disable-ipc-flooding-protection",
                "--disable-prompt-on-repost",
                "--disable-renderer-backgrounding",
                "--disable-sync",
                "--disable-web-resources",
                "--enable-automation",
                "--enable-blink-features=IdleDetection",
                "--enable-features=NetworkService,NetworkServiceInProcess",
                "--force-color-profile=srgb",
                "--metrics-recording-only",
                "--no-first-run",
                "--password-store=basic",
                "--use-mock-keychain",
                "--enable-features=DisableChromiumDriverWarning",
                "--disable-features=AutomationWarning",
                "--disable-features=BrowserNotificationAutomation",
            ],
            env={
                "GOOGLE_CHROME_PINNED_TASKBAR_HIGHLIGHT": "0",  # Remove taskbar highlight
                "CHROME_LOG_FILE": "nul",  # Suppress log output
            },
            user_agent=self.random_user_agent(),
        )
        self.page = (
            self.browser.pages[0]
            if self.browser.pages
            else await self.browser.new_page()
        )

        await self.page.set_viewport_size({"width": 1400, "height": 950})

        await self.page.evaluate(
            """
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => false});
                Object.defineProperty(navigator, 'language', { value: 'en-US' });
                Object.defineProperty(navigator, 'plugins', { value: [] });
                Object.defineProperty(navigator, 'hardwareConcurrency', { value: 4 });
                window.navigator.chrome = {runtime: {},};
                screen.width = 1920;
                screen.height = 1080;
                window.devicePixelRatio = 1;
                navigator.cpuClasses = ['desktop', 'low-end'];
            }
            """
        )

    def random_user_agent(self):
        return self.ua.random

    async def close_browser(self):
        try:
            # Attempt to close pages individually
            if self.browser and hasattr(self.browser, "pages"):
                for page in self.browser.pages:
                    try:
                        if not page.is_closed():
                            await asyncio.wait_for(page.close(), timeout=5.0)
                    except Exception as page_error:
                        print(f"Error closing page: {page_error}")

            # Attempt to close the browser context
            if self.browser:
                try:
                    await asyncio.wait_for(self.browser.close(), timeout=10.0)
                except Exception as browser_error:
                    print(f"Error closing browser: {browser_error}")

            # Stop the playwright instance
            if self.playwright:
                try:
                    await asyncio.wait_for(self.playwright.stop(), timeout=10.0)
                except Exception as playwright_error:
                    print(f"Error stopping playwright: {playwright_error}")

        except Exception as e:
            print(f"Unexpected error during browser closure: {e}")
        finally:
            # Force garbage collection to release any lingering references
            import gc

            gc.collect()

            # Clear all references
            self.page = None
            self.browser = None
            self.playwright = None

        # Allow event loop to process any pending events
        await asyncio.sleep(0)

    async def ai_to_run_driver(self, ai_to_run):

        match ai_to_run:

            case AIList.CHATGPT.value:
                return await self.run_ai("https://chatgpt.com/", "#prompt-textarea", 2)

            case AIList.META_AI.value:
                return await self.run_ai(
                    "https://www.meta.ai/",
                    "//textarea[@placeholder='Ask Meta AI anything...']",
                )
            case AIList.GEMINI.value:
                return await self.run_ai("https://gemini.google.com/", ".ql-editor")
            case _:
                return await self.run_ai(
                    "https://copilot.microsoft.com/", "cib-text-input", 2
                )

    async def run_ai(self, url, locator, sleep_time=0):
        await self.launch_browser()
        await self.page.goto(url)

        if url == "https://copilot.microsoft.com/":
            self.page.get_by_role("radio", name="More Precise")

        text_area = self.page.locator(locator)
        await text_area.focus()
        await asyncio.sleep(sleep_time)
        await text_area.press("Control+V")
        await asyncio.sleep(sleep_time)
        await text_area.press("Enter")
        # input("Press Enter to Exit...")
        # await self.close_browser()


if __name__ == "__main__":

    helper = PlaywrightHelper()

    asyncio.run(helper.ai_to_run_driver(AIList.CHATGPT.value))
