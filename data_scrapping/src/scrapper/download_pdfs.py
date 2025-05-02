import os
import time
import re
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        prefs = {"download.default_directory": os.getcwd()}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def fetch_quarterly_pdfs(self, company_symbol):
        base_url = f"https://www.cse.lk/pages/company-profile/company-profile.component.html?symbol={company_symbol}.N0000"
        self.driver.get(base_url)

        try:
            financials_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Financials')]"))
            )
            financials_tab.click()
            time.sleep(2)
        except Exception as e:
            print("Financials tab not found:", e)
            return []

        try:
            quarterly_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Quarterly Reports')]"))
            )
            quarterly_tab.click()
            time.sleep(2)
        except Exception as e:
            print("Quarterly Reports tab not found:", e)
            return []

        pdf_links = []
        current_year = datetime.now().year

        try:
            rows = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@class='data-table']//tbody//tr"))
            )
            for row in rows:
                try:
                    report_text = row.text.lower()
                    print("ROW TEXT:", report_text)

                    if any(keyword in report_text for keyword in ["quarterly", "interim", "3 months", "six months"]):
                        year = self.extract_year(report_text)
                        if year and (current_year - 4 <= year <= current_year):
                            pdf_icon = row.find_element(By.XPATH, ".//a[contains(@href, '.pdf')]")
                            pdf_url = pdf_icon.get_attribute("href")
                            if pdf_url:
                                print(f"Found report ({year}): {pdf_url}")
                                pdf_links.append(pdf_url)
                        else:
                            print(f"Ignored old or undated report: {report_text}")
                except Exception as e:
                    print(f"Error extracting row: {e}")
        except Exception as e:
            print(f"Error finding table rows: {e}")

        self.download_pdf(pdf_links, company_symbol)
        return pdf_links

    def extract_year(self, text):
        """Extract year from text, return as int if found, else None"""
        match = re.search(r'(20\d{2})', text)
        if match:
            return int(match.group(1))
        return None

    def download_pdf(self, pdf_urls, company_symbol):
        # Use project root path: go two levels up from this script
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        output_dir = os.path.join(project_root, "data", "raw", company_symbol)
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []

        for idx, pdf_url in enumerate(pdf_urls):
            try:
                if not pdf_url.startswith("http"):
                    print(f"Invalid URL: {pdf_url}")
                    continue

                response = requests.get(pdf_url)
                if response.status_code == 200:
                    filename = f"{company_symbol}_quarterly_{idx + 1}.pdf"
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    saved_paths.append(filepath)
                    print(f"Downloaded: {filepath}")
                else:
                    print(f"Failed to download PDF: {pdf_url} (status {response.status_code})")
            except Exception as e:
                print(f"Error downloading {pdf_url}: {e}")

        return saved_paths

    def close(self):
        self.driver.quit()


