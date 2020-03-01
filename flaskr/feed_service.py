import sqlalchemy

from . import models
from . import db
from .utils import feedparser


def search(q: str) -> list:
    if not is_source_exists(q) and _is_link(q):
        _discover_source(q)

    result = models.Source.query.filter(sqlalchemy.or_(models.Source.feed_link==q, models.Source.url==q))
    return result


def is_source_exists(q: str) -> bool:
    # TODO: implement
    return False


def _is_link(q: str):
    # TODO: implement
    return True


def _discover_source(link: str):
    source_record = models.Source.query.filter_by(feed_link=link).first()
    if source_record:
        return

    parser = feedparser.FeedParser(link)
    source = models.Source(**parser.source)
    db.session.add(source)
    db.session.commit()