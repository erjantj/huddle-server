from urllib import parse
import re


url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_base_url(url: str) -> str:
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parse.urlparse(url))
    return base_url.replace("://www.","://")


def is_url(string: str) -> bool:
    return re.match(url_regex, string) is not None