from . import ma

class SearchSchema(ma.Schema):
    class Meta:
        fields = ('url',)

class SourceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'url', 'feed_link', 'icon', 'language')

    # _links = ma.Hyperlinks(
    #     {'self': ma.URLFor('user_detail'), 'collection': ma.URLFor('users')}
    # )


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email')


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'link', 'author', 'published_at', 'source')
    source = ma.Nested(SourceSchema)