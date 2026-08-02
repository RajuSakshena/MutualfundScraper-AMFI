import requests

from playwright.sync_api import sync_playwright

from config import *


class AMFIDownloader:

    def __init__(self):

        self.download_dir = DOWNLOAD_DIR

    def get_latest_excel_url(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=HEADLESS
            )

            context = browser.new_context(
                user_agent=USER_AGENT
            )

            page = context.new_page()

            print("Opening AMFI...")

            page.goto(
                AMFI_URL,
                wait_until="networkidle",
                timeout=TIMEOUT
            )

            # Monthly dropdown

            page.locator(
                'div[role="combobox"]'
            ).click()

            page.get_by_role(
                "option",
                name="AMFI Monthly Data"
            ).click()

            page.wait_for_timeout(1500)

            # Latest Excel URL

            url = page.locator(
                'a[href$=".xls"]'
            ).first.get_attribute("href")

            browser.close()

            if not url:

                raise Exception("Latest Excel URL not found.")

            print(url)

            return url

    def download_excel(self):

        url = self.get_latest_excel_url()

        filename = url.split("/")[-1]

        filepath = self.download_dir / filename

        if filepath.exists():

            print("Already Exists")

            return filepath

        print("Downloading...")

        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=60
        )

        response.raise_for_status()

        filepath.write_bytes(response.content)

        print("Downloaded Successfully")

        return filepath