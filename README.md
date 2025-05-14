# Habby Store Price Scraper

This project scrapes gem prices from the Habby store for multiple countries using Playwright and authenticated proxies (Oxylabs). It extracts dynamically rendered price data and saves results to a CSV file.

## Features
- Scrapes https://store.habby.com/game/4 for major regions
- Uses Playwright for reliable dynamic content extraction
- Authenticated proxy support (Oxylabs)
- Results saved to `data/results_by_country.csv`

## Setup
1. **Clone the repo and install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. **Configure your Oxylabs credentials:**
   - Copy `.env.example` to `.env` and fill in your `OXYLABS_USER` and `OXYLABS_PASS`.

## Usage
Run the scraper:
```bash
python main.py
```
- By default, all supported country codes are scraped. You can edit the `COUNTRY_CODES` list in `main.py` to limit countries.

## Output
- Results are saved to `data/results_by_country.csv` with columns: `country`, `price`, `currency`, `raw_button_text`.

## View Cleaned Data
You can view the cleaned and converted price data (best prices in euros) at this Google Sheets link:
[View Cleaned Data](https://docs.google.com/spreadsheets/d/1I5tkjVzS70u_2ywnUJYRQnFFZ3vCkA7Fqs1z1h56E90/edit?usp=sharing)

## Notes
- Requires Python 3.8+
- Make sure your Oxylabs account is active and allows the required geographies.
- For troubleshooting proxy or scraping issues, check your `.env` and proxy permissions.
