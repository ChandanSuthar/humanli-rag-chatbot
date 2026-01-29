import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class WebCrawler:
    def __init__(self, base_url: str, max_pages: int = 5):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.visited_urls = set()

    def crawl(self) -> list[dict]:
        """
        Crawls the base URL and shallow internal links (depth = 1).
        """
        pages_data = []
        urls_to_visit = [self.base_url]

        while urls_to_visit and len(self.visited_urls) < self.max_pages:
            current_url = urls_to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            try:
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
            except requests.RequestException:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            self.visited_urls.add(current_url)

            page_text = self._extract_text(soup)
            page_title = soup.title.string.strip() if soup.title else ""

            pages_data.append({
                "text": page_text,
                "source_url": current_url,
                "title": page_title
            })

            internal_links = self._extract_internal_links(soup)
            urls_to_visit.extend(internal_links)

        return pages_data

    def _extract_text(self, soup: BeautifulSoup) -> str:
        texts = []

        for tag in soup.find_all(["p", "li", "h1", "h2", "h3"]):
            text = tag.get_text(strip=True)
            if text:
                texts.append(text)

        return "\n".join(texts)

    def _extract_internal_links(self, soup: BeautifulSoup) -> list[str]:
        links = []

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            full_url = urljoin(self.base_url, href)
            parsed = urlparse(full_url)

            if parsed.netloc == self.domain:
                links.append(full_url)

        return links
