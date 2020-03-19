import sqlalchemy

from . import models
from . import db
from . import errors
from . import celery
from .utils import feedparser
from sqlalchemy import sql
import re

POSTS_PER_PAGE = 10


def search(q: str) -> list:
    source_records = search_source(q)
    if not source_records and _is_link(q):
        discover_source(q)
        return models.Source.query.filter(sqlalchemy.or_(models.Source.feed_link==q, models.Source.url==q))
    return source_records
    

def subscribe(user, source_id):
    source_record = models.Source.query.filter_by(id=source_id).first()
    if not source_record:
        raise errors.SourceNotFoundError()

    source_subscription = models.SourceSubscription.query.filter(models.SourceSubscription.user_id==user.id, models.SourceSubscription.source_id==source_id).first()
    if source_subscription:
        return

    source_subscription = models.SourceSubscription(user_id=user.id, source_id=source_id)
    db.session.add(source_subscription)
    db.session.commit()


def feed(user, page:int=1) -> list:
    source_subscriptions = models.SourceSubscription.query.filter_by(user_id=user.id).all()
    source_ids = (subscription.source_id for subscription in source_subscriptions)
    return models.Post.query.filter(models.Post.source_id.in_(source_ids)).order_by(models.Post.published_at.desc()).paginate(page, POSTS_PER_PAGE, False).items


def search_source(q: str) -> bool:
    words = re.sub(r'\W+', '', q).split()
    value = '* '.join(words)+'*' if words else ''
    condition = sql.text("MATCH (name,description,url,feed_link) AGAINST (:value IN BOOLEAN MODE)",
            bindparams=[sql.bindparam('value', value)])
    source_records = models.Source.query.filter(condition)
    print(models.Source.query.filter(condition).statement.compile())
    print('* '.join(words))
    return source_records


def discover_source(link: str):
    source_record = models.Source.query.filter_by(feed_link=link).first()
    if source_record:
        return

    parser = feedparser.FeedParser(link)
    source = models.Source(**parser.source)
    db.session.add(source)
    db.session.commit()

    fetch_latest_feed.delay(source.id)
    

@celery.task
def fetch_latest_feed(source_id: int):
    source = models.Source.query.filter_by(id=source_id).first()
    parser = feedparser.FeedParser(source.feed_link)
    
    links = (entry['link'] for entry in parser.entries)
    post_records = models.Post.query.filter(models.Post.id.in_(links)).all()
    existing_links = {post.link for post in post_records}

    posts = []
    for entry in parser.entries:
        if entry['title'] and entry['link'] not in existing_links:
            post = models.Post(**entry)
            post.source_id = source_id
            posts.append(post)
    db.session.bulk_save_objects(posts)
    db.session.commit()

def _is_link(q: str):
    # TODO: implement
    return True


