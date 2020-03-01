from . import ma

class SearchSchema(ma.Schema):
    class Meta:
        fields = ('url',)

class SourceSchema(ma.Schema):
    class Meta:
        fields = ('name', 'description', 'url', 'feed_link', 'icon', 'language')

    # _links = ma.Hyperlinks(
    #     {'self': ma.URLFor('user_detail'), 'collection': ma.URLFor('users')}
    # )
