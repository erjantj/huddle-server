import sqlalchemy

from flaskr import models
from flaskr import db
from flaskr import errors
from flaskr import helpers
from flaskr import celery
from flaskr.utils import feedparser
from sqlalchemy import sql
import bs4
import re
import urllib


POSTS_PER_PAGE = 10


def search(q: str) -> list:
    is_url = helpers.is_url(q)
    if is_url:
        q = helpers.get_base_url(q)

    source_records = search_source(q)
    if not source_records and is_url:
        discover_source(q)
        url = helpers.get_base_url(q)
        return models.Source.query.filter_by(url=url).all()
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
    source_records = models.Source.query.filter(condition).all()
    return source_records


def discover_source(link: str):
    source_record = models.Source.query.filter(sqlalchemy.or_(models.Source.feed_link==link, models.Source.url==link)).all()
    if source_record:
        return
        
    sources = []
    feed_links = [link]
    # Try to get RSS feed from link.
    parser = feedparser.FeedParser()
    data = parser.parse_source(link)
    if not data['source'] or not data['source']['name']:
        # If no RSS source found, try to find link on page.
        feed_links = discover_link(link)

    for feed_link in feed_links:
        data = parser.parse_source(feed_link)
        if not data['source'] or not data['source']['name']:
            continue
        source = models.Source(**data['source'])
        sources.append(source)

    db.session.bulk_save_objects(sources)
    db.session.commit()

    for source in sources:
        fetch_latest_feed.delay(source.url)
    

@celery.task
def fetch_latest_feed(source_url: str):
    source = models.Source.query.filter_by(url=source_url).first()
    if not source:
        raise errors.SourceNotFoundError()
    parser = feedparser.FeedParser()
    data = parser.parse_source(source.feed_link)
    
    links = (entry['link'] for entry in data['entries'])
    post_records = models.Post.query.filter(models.Post.id.in_(links)).all()
    existing_links = {post.link for post in post_records}

    posts = []
    for entry in data['entries']:
        if entry['title'] and entry['link'] not in existing_links:
            post = models.Post(**entry)
            post.source_id = source.id
            posts.append(post)
    db.session.bulk_save_objects(posts)
    db.session.commit()


def discover_link(link: str) -> list:
    possible_feeds = []
    try:
        page = urllib.request.urlopen(link).read()
        html = bs4.BeautifulSoup(page, "html.parser")
        feeds = html.findAll(type='application/rss+xml') + html.findAll(type='application/atom+xml')
        for feed in feeds:
            href = feed.get("href",None)
            if not href:
                continue
            possible_feeds.append(href)
    except urllib.error.URLError:
        raise errors.SourceParseError()

    return possible_feeds

