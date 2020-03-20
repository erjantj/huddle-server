from flaskr import ma


class SearchSchema(ma.Schema):
    class Meta:
        fields = ('url',)

class SourceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'url', 'feed_link', 'icon', 'language')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email')


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'link', 'author', 'published_at', 'source')
    source = ma.Nested(SourceSchema)