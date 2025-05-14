import pandas as pd
import os
from dotenv import load_dotenv
import asyncio

STORE_URL = "https://store.habby.com/game/4"

# Practical, widely-used country codes (skipping regions rarely used for gaming/VPN)
COUNTRY_CODES = [
    'US', 'GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'CA', 'AU', 'IN', 'BR', 'MX', 'TR', 'RU', 'JP', 'KR', 'SG', 'ID', 'TH', 'VN', 'PH', 'MY', 'PL', 'SE', 'NO', 'FI', 'DK', 'ZA', 'SA', 'AE', 'AR', 'CL', 'CO', 'NZ', 'IE', 'PT', 'GR', 'CZ', 'HU', 'RO', 'SK', 'CH', 'AT', 'UA', 'IL', 'HK', 'TW'
]

# For testing:
# COUNTRY_CODES = ['US']

load_dotenv()
OXYLABS_USER = os.getenv('OXYLABS_USER')
OXYLABS_PASS = os.getenv('OXYLABS_PASS')


async def fetch_prices_with_playwright(url, country_code, oxylabs_user, oxylabs_pass):
    from playwright.async_api import async_playwright
    proxy = {
        "server": "http://pr.oxylabs.io:7777",
        "username": f"customer-{oxylabs_user}-cc-{country_code}",
        "password": oxylabs_pass
    }
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(proxy=proxy, user_agent=user_agent)
        page = await context.new_page()
        try:
            await page.goto(url, timeout=60000)
            # Wait for the price buttons to appear
            await page.wait_for_selector('.button', timeout=20000)
            print(f"[DEBUG] Price button(s) detected for {country_code}!")
            # Extract price data
            buttons = await page.query_selector_all('.button')
            data = []
            import re
            for btn in buttons:
                text = (await btn.inner_text()).strip()
                if not text:
                    continue
                match = re.search(r'(\d+[.,]?\d*)\s*([A-Z]{2,4})', text)
                if match:
                    price = match.group(1)
                    currency = match.group(2)
                else:
                    price = text
                    currency = ''
                data.append({
                    'country': country_code,
                    'price': price,
                    'currency': currency,
                    'raw_button_text': text
                })
            return data
        except Exception as e:
            print(f"Error for {country_code}: {e}")
            return []
        finally:
            await context.close()
            await browser.close()

async def main():
    all_data = []
    for country in COUNTRY_CODES:
        print(f"Scraping for {country}...")
        prices = await fetch_prices_with_playwright(STORE_URL, country, OXYLABS_USER, OXYLABS_PASS)
        if prices:
            all_data.extend(prices)
        else:
            print(f"No prices found for {country}")
    if all_data:
        df = pd.DataFrame(all_data)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/results_by_country.csv", index=False)
        print(f"Done! Results saved to data/results_by_country.csv")
    else:
        print("No data scraped.")

if __name__ == "__main__":
    asyncio.run(main())


