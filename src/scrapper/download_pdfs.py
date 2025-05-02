import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def fetch_quarterly_pdfs_dict(url: str, wait_time: int = 5) -> dict:
    """
    Scrape PDF links for quarterly/interim financial reports and return a dict of {date: pdf_link},
    but only for reports within the last 4 years.
    """
    pdf_dict = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(wait_time)

        rows = driver.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            text = row.text.lower()

            # Match broader variations of quarterly/interim reports
            if any(keyword in text for keyword in ["quarterly financial report", "interim financial statement"]):
                try:
                    link_element = row.find_element(By.XPATH, './/a[contains(@href, ".pdf")]')
                    href = link_element.get_attribute("href")
                except:
                    continue

                raw_date = None
                if "as at" in text:
                    raw_date = text.split("as at")[-1].strip()
                elif "as of" in text:
                    raw_date = text.split("as of")[-1].strip()
                else:
                    # Try extracting the last date-like token with dots (e.g., 31.12.2024)
                    for token in reversed(text.split()):
                        if any(char.isdigit() for char in token) and "." in token:
                            raw_date = token.strip()
                            break

                if not raw_date:
                    print(f"Could not extract date from: {text}")
                    continue

                parsed = None
                for fmt in ("%d-%m-%Y", "%d.%m.%Y", "%d.%m.%y", "%d/%m/%Y", "%d-%m-%y", "%d-%b-%Y"):
                    try:
                        parsed = datetime.strptime(raw_date, fmt)
                        break
                    except ValueError:
                        continue

                if parsed:
                    year = parsed.year
                    current_year = datetime.now().year
                    if current_year - 4 <= year <= current_year:
                        norm_date = parsed.strftime("%Y-%m-%d")
                        pdf_dict[norm_date] = href
                    else:
                        print(f"Ignored old report: {parsed.date()}")
                else:
                    print(f"Could not parse date: {raw_date}")
    finally:
        driver.quit()

    return pdf_dict

def download_pdfs(pdf_dict: dict, company_symbol: str):
    """
    Download all PDFs given a dict of {date: url}.
    """
    output_folder = f"./data/raw/{company_symbol}"
    os.makedirs(output_folder, exist_ok=True)

    for date, url in pdf_dict.items():
        filename = f"{company_symbol}_{date}.pdf"
        filepath = os.path.join(output_folder, filename)
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {filename} - Status {resp.status}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

def main():
    companies = {
        "DIPD": "https://www.cse.lk/pages/company-profile/company-profile.component.html?symbol=DIPD.N0000",
        "REXP": "https://www.cse.lk/pages/company-profile/company-profile.component.html?symbol=REXP.N0000",
    }

    for symbol, url in companies.items():
        print(f"Fetching reports for {symbol}")
        pdf_links = fetch_quarterly_pdfs_dict(url)
        print(f"Found {len(pdf_links)} reports for {symbol}")
        download_pdfs(pdf_links, symbol)

if __name__ == "__main__":
    main()
