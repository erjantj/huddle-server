"""Application helper functions."""
from urllib import parse
import re


URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
    r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_base_url(url: str) -> str:
    """Gets base url from link.

    Args:
      url: A url string.

    Returns:
        Base url string.
    """
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parse.urlparse(url))
    return base_url.replace("://www.", "://")


def is_url(string: str) -> bool:
    """Checks is given string is url.

    Args:
      string: A target string.

    Returns:
        True if given string is url.
    """
    return re.match(URL_REGEX, string) is not None
