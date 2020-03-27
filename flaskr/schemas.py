"""Response data schemas."""
from flaskr import ma


# pylint: disable=too-few-public-methods
class SearchSchema(ma.Schema):
    """Search response schema."""

    class Meta:
        """Meta class."""
        fields = ('url',)


class SourceSchema(ma.Schema):
    """Source response schema."""
    class Meta:
        """Meta class."""
        fields = ('id', 'name', 'description', 'url',
                  'feed_link', 'icon', 'language')


class UserSchema(ma.Schema):
    """User response schema."""
    class Meta:
        """Meta class."""
        fields = ('username', 'email')


class PostSchema(ma.Schema):
    """Post response schema."""
    class Meta:
        """Meta class."""
        fields = ('id', 'title', 'content', 'link',
                  'author', 'published_at', 'source')
    source = ma.Nested(SourceSchema)
