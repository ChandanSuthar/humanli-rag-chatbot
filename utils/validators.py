from urllib.parse import urlparse


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validates whether the input is a proper HTTP/HTTPS URL.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """

    if not url or not url.strip():
        return False, "URL cannot be empty."

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False, "URL must start with http:// or https://"

    if not parsed.netloc:
        return False, "Invalid URL format."

    return True, ""
