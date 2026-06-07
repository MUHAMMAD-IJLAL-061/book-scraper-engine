# book-scraper-engine
# E-Commerce Book Scraper Engine

A modular, object-oriented Python command-line utility engineered to scrape product details across multi-page e-commerce architectures.

## Features
- **Object-Oriented Design:** Segregates data entities (`Book`) from orchestration logic (`BookScraper`).
- **Connection Pooling:** Utilizes `requests.Session()` to persist TCP connections, optimizing scraping speed and reducing server overhead.
- **Robust Pagination:** Dynamically tracks and resolves relative pagination URLs safely via `urllib.parse.urljoin`.
- **Data Normalization:** Sanitizes currency symbols and extracts star-rating HTML classes into structured float and integer formats before exporting to CSV.

## Tech Stack
- Python 3
- BeautifulSoup4
- Requests

## How to Run
1. Clone the repository: `git clone https://github.com/MUHAMMAD-IJLAL-061/book-scraper-engine.git`
2. Install dependencies: `pip install beautifulsoup4 requests`
3. Run the script: `python scraper.py`
