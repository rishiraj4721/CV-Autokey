
import requests
from bs4 import BeautifulSoup

from .cache import json_cache

@json_cache()
def get_text_from_url(url):
    """Attempt to scrape, return None if it fails or looks like a login page.
    Results are cached to avoid repeated scraping of the same URL."""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        print(f"[Scraping] Fetching job description from {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch {url}, status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Clean up the soup
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        # If the scraped text is suspiciously short, it likely failed to bypass a wall
        if len(text) > 200:
            return text
        raise ValueError(f"Scraped content from {url} is too short: {text}")
    except Exception as e:
        raise ValueError(f"[Scraping] Error fetching {url}: {e}")