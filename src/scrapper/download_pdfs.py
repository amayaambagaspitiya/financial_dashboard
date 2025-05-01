import aiohttp
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import os

async def fetch_quarterly_pdfs_dict(url: str, timeout_duration: int) -> dict:
    """
    Scrape PDF links for quarterly/interim financial reports and return a dict of {date: pdf_link}.
    """
    pdf_dict = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(timeout_duration)

        rows = await page.query_selector_all("tr")
        for row in rows:
            text = await row.inner_text()

              #Match both DIPD and REXP formats
            if ("Quarterly Financial report as of" in text) or ("Interim Financial Statement" in text):
                link = await row.query_selector('a[href$=".pdf"]')
                if not link:
                    continue
                href = await link.get_attribute('href')

                # Extract raw date
                raw_date = None
                if "as at" in text:
                    raw_date = text.split("as at")[-1].strip()
                elif "-" in text:
                    parts = text.split("-")
                    if len(parts) >= 2:
                        raw_date = parts[-1].strip()

                if not raw_date:
                    print(f"⚠️ Could not extract date from: {text}")
                    continue

                # Try parsing with multiple formats
                parsed = None
                for fmt in ("%d-%m-%Y", "%d.%m.%Y", "%d.%m.%y", "%d/%m/%Y", "%d-%m-%y", "%d-%b-%Y", "%d.%m.%Y"):
                    try:
                        parsed = datetime.strptime(raw_date, fmt)
                        break
                    except ValueError:
                        continue

                if parsed:
                    norm_date = parsed.strftime("%Y-%m-%d")
                    pdf_dict[norm_date] = href
                else:
                    print(f"Could not parse date: {raw_date}")

        await browser.close()
    return pdf_dict

async def download_pdfs(pdf_dict: dict, company_symbol: str):
    """
    Download all PDFs given a dict of {date: url}.
    """
    output_folder = f"./data/raw/{company_symbol}"
    os.makedirs(output_folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        for date, url in pdf_dict.items():
            filename = f"{company_symbol}_{date}.pdf"
            filepath = os.path.join(output_folder, filename)
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open(filepath, 'wb') as f:
                            f.write(await resp.read())
                        print(f" Downloaded {filename}")
                    else:
                        print(f"Failed to download {filename} - Status {resp.status}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")

async def main():
    companies = {
        "DIPD": "https://www.cse.lk/pages/company-profile/company-profile.component.html?symbol=DIPD.N0000",
        "REXP": "https://www.cse.lk/pages/company-profile/company-profile.component.html?symbol=REXP.N0000",
    }

    for symbol, url in companies.items():
        print(f"🔎 Fetching reports for {symbol}")
        pdf_links = await fetch_quarterly_pdfs_dict(url, timeout_duration=5000)
        print(f"Found {len(pdf_links)} reports for {symbol}")
        await download_pdfs(pdf_links, symbol)

if __name__ == "__main__":
    asyncio.run(main())
