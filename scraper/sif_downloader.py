import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

SIF_URL = "https://www.amfiindia.com/sif/sif-monthly"

DOWNLOAD_DIR = Path("downloads/sif")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

HEADLESS = True
TIMEOUT = 60000


class SIFDownloader:

    def get_latest_excel_url(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=HEADLESS)

            page = browser.new_page()

            print("Opening SIF Monthly...")

            page.goto(
                SIF_URL,
                wait_until="networkidle",
                timeout=TIMEOUT
            )

            page.locator('a[href$=".xls"]').first.wait_for()

            url = page.locator(
                'a[href$=".xls"]'
            ).first.get_attribute("href")

            browser.close()

            if not url:
                raise Exception("SIF Excel URL not found.")

            url = url.replace("\\", "/")

            print("Latest Excel :", url)

            return url

    def download_excel(self):

        url = self.get_latest_excel_url()

        filename = url.split("/")[-1]

        filepath = DOWNLOAD_DIR / filename

        if filepath.exists():

            print("Already Exists")

            return filepath

        print("Downloading...")

        r = requests.get(
            url,
            timeout=60
        )

        r.raise_for_status()

        filepath.write_bytes(r.content)

        print("Downloaded Successfully")

        return filepath
