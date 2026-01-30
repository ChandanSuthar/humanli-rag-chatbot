import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.config import Config

class WebsiteCrawler:
    def __init__(self):
        self.headers = {'User-Agent': Config.USER_AGENT}

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_content(self, url):
        """
        Fetches text content from a URL.
        Returns: Cleaned text string or None if failed.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements that confuse RAG
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            
            # Get text and clean whitespace
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return clean_text
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return None