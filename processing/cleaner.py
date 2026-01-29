from bs4 import BeautifulSoup


def clean_html(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes non-content elements from HTML to reduce noise
    before text extraction.
    """

    # Remove common non-content tags
    for tag_name in ["header", "footer", "nav", "aside", "script", "style"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Remove common ad / cookie / popup sections by keywords
    noise_keywords = [
        "cookie",
        "consent",
        "advertisement",
        "ads",
        "promo",
        "banner",
        "subscribe",
        "newsletter"
    ]

    for div in soup.find_all("div"):
        class_id = " ".join(div.get("class", [])) + " " + (div.get("id") or "")
        class_id = class_id.lower()

        if any(keyword in class_id for keyword in noise_keywords):
            div.decompose()

    return soup
