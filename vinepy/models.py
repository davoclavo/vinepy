import json
from datetime import datetime

from errors import *

def strptime(string, fmt='%Y-%m-%dT%H:%M:%S.%f'):
    return datetime.strptime(string, fmt)


class DummyAPI():
    def __getattr__(self, name):
        raise NotImplementedError('This model does not have an API instance associated with it.')


class DummyUser():
    def __getattr__(self, name):
        raise NotImplementedError("This API instance does not have an authenticated user, try logging in or signing up.")


# From http://stackoverflow.com/a/14620633
# CAUTION: it causes memory leak in < 2.7.3 and < 3.2.3
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Model(AttrDict):
    api = DummyAPI()

    @classmethod
    def from_json(cls, data):
        self = cls(data)
        self['json'] = json.dumps(data)
        return self

    def connect_api(self, api):
        self.api = api


class ModelCollection(list):
    model = Model

    @classmethod
    def from_json(cls, data):
        self = cls()
        for item in data:
            self.append(self.model.from_json(item))
        return self

    def connect_api(self, api):
        for item in self:
            item.connect_api(api)

    def __iter__(self):
        self._iterator = list.__iter__(self)
        return self._iterator

    def next(self):
        return self._iterator.next()


# Model collection with metadata
class MetaModelCollection(Model):
    model_key = 'records'
    collection_class = ModelCollection

    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            if key == self.model_key:
                value = self.collection_class.from_json(value)
            self[key] = value
        return self

    def connect_api(self, api):
        for item in self.get_collection():
            item.connect_api(api)

    def __len__(self):
        return len(self.get_collection())

    def __getitem__(self, descriptor):
        # Retrieving an attribute
        if type(descriptor) in [str, unicode]:
            return Model.__getitem__(self, descriptor)

        # Retrieving an element from the list
        else:
            return self.get_collection().__getitem__(descriptor)

    def __iter__(self):
        return self.get_collection().__iter__()

    def __repr__(self):
        return self.get_collection().__repr__()

    def next(self):
        return self.get_collection().next()

    def get_collection(self):
        return self.get(self.model_key, [])

# User decorator
def only_me(fn):
    def _decorator(self, *args, **kwargs):
        if('key' in self.keys()):
            return fn(self, *args, **kwargs)
        else:
            # raise VineError(4, "You don't have permission to access that record.")
            raise VineError(1337, "Only %s can access this record." % self)
    return _decorator

class User(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            self[key] = value

        if(self['userId']):
            self['id'] = self['userId']
            del self['userId']

        return self

    def __repr__(self):
        return "User[%s:%s]" % (self.id, self.username)

    def connect_api(self, api):
        self.api = api
        if('key' in self.keys()):
            self.api.authenticate(self)

    def follow(self, **kwargs):
        return self.api.follow(user_id=self.id, **kwargs)

    def unfollow(self, **kwargs):
        return self.api.unfollow(user_id=self.id, **kwargs)

    def block(self, **kwargs):
        return self.api.block(user_id=self.id, **kwargs)

    def unblock(self, **kwargs):
        return self.api.unblock(user_id=self.id, **kwargs)

    def followers(self, **kwargs):
        return self.api.get_followers(user_id=self.id, **kwargs)

    def following(self, **kwargs):
        return self.api.get_following(user_id=self.id, **kwargs)

    def timeline(self, **kwargs):
        return self.api.get_user_timeline(user_id=self.id, **kwargs)

    def likes(self, **kwargs):
        return self.api.get_user_likes(user_id=self.id, **kwargs)

    @only_me
    def pending_notifications_count(self, **kwargs):
        # if('key' in self.keys()):
        return self.api.get_pending_notifications_count(user_id=self.id, **kwargs)

    @only_me
    def notifications(self, **kwargs):
        # if('key' in self.keys()):
        return self.api.get_notifications(user_id=self.id, **kwargs)

    @only_me
    def update(self, **kwargs):
        return self.api.update_user(user_id=self.id, **kwargs)

    @only_me
    def set_explicit(self, **kwargs):
        return self.api.set_explicit(user_id=self.id, **kwargs)

    @only_me
    def unset_explicit(self, **kwargs):
        return self.api.unset_explicit(user_id=self.id, **kwargs)


class Post(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            if key == 'created':
                value = strptime(value)
            elif key == 'comments':
                value = CommentCollection.from_json(value)
                pass
            elif key == 'likes':
                value = LikeCollection.from_json(value)
                pass
            elif key == 'reposts':
                value = RepostCollection.from_json(value)
                pass
            elif key == 'tags':
                value = PureTagCollection.from_json(value)
                pass
            elif key == 'user':
                value = User.from_json(value)
            self[key] = value

        if(self['postId']):
            self['id'] = self['postId']
            del self['postId']

        return self

    def __repr__(self):
        chars = 10
        return 'Post[%s:%s]' % (self.id, self.description[:chars] + (self.description[chars:] and '...'))

    def like(self, **kwargs):
        return self.api.like(post_id=self.id, **kwargs)

    def unlike(self, **kwargs):
        return self.api.unlike(post_id=self.id, **kwargs)

    def revine(self, **kwargs):
        return self.api.revine(post_id=self.id, **kwargs)

    def comment(self, **kwargs):
        return self.api.comment(post_id=self.id, **kwargs)

    # def uncomment(self, **kwargs):
    #     return self.api.comment(post_id=self.id, **kwargs)

    def report(self, **kwargs):
        return self.api.report(post_id=self.id, **kwargs)


class Comment(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            if key == 'created':
                value = strptime(value)
            elif key == 'entities':
                # value = EntityCollection.from_json(value)
                pass
            elif key == 'user':
                value = User.from_json(value)
            self[key] = value

        if(self['commentId']):
            self['id'] = self['commentId']
            del self['commentId']

        return self

    def __repr__(self):
        chars = 10
        return 'Comment[[%s:%s]:%s]' % (self.id, self.comment[:chars] + (self.comment[chars:] and '...'), self.post)

    def delete(self, **kwargs):
        return self.api.uncomment(post_id=self.post.id, comment_id=self.id, **kwargs)


class Like(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            if key == 'created':
                value = strptime(value)
            elif key == 'user':
                value = User.from_json(value)
            self[key] = value

        if(self['likeId']):
            self['id'] = self['likeId']
            del self['likeId']

        return self

    def __repr__(self):
        chars = 10
        return 'Like[%s:%s]' % (self.id, self.post)

    def delete(self, **kwargs):
        return self.api.unlike(post_id=self.post.id, **kwargs)


class Repost(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            if key == 'created':
                value = strptime(value)
            elif key == 'user':
                value = User.from_json(value)
            self[key] = value

        if(self['repostId']):
            self['id'] = self['repostId']
            del self['repostId']

        return self

    def __repr__(self):
        chars = 10
        return 'Repost[%s:%s]' % (self.id, self.post)

    def delete(self, **kwargs):
        return self.api.unrevine(post_id=self.post.id, revine_id=self.id, **kwargs)

class Tag(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            self[key] = value

        if(self['tagId']):
            self['id'] = self['tagId']
            del self['tagId']

        return self

    def __repr__(self):
        return 'Tag[%s:%s]' % (self.id, self.tag)

    def timeline(self):
        return self.api.get_tag_timeline(tag_name=self.tag, **kwargs)


class Channel(Model):
    @classmethod
    def from_json(cls, data):
        self = cls(Model.from_json(data))
        for key, value in self.iteritems():
            if key == 'created':
                value = strptime(value)
            self[key] = value

        if(self['channelId']):
            self['id'] = self['channelId']
            del self['channelId']

        return self

    def __repr__(self):
        return 'Channel[%s:%s]' % (self.id, self.channel)

    def timeline(self):
        return self.api.get_channel_recent_timeline(channel_id=self.id, **kwargs)

    def recent_timeline(self):
        return self.timeline()

    def popular_timeline(self):
        return self.api.get_channel_popular_timeline(channel_id=self.id, **kwargs)

# mention, tag or post in a notification, comment or title
class Entity(Model):
    pass


class Venue(Model):
    pass


class PureUserCollection(ModelCollection):
    model = User


class UserCollection(MetaModelCollection):
    collection_class = PureUserCollection


class PurePostCollection(ModelCollection):
    model = Post


# Timeline
class PostCollection(MetaModelCollection):
    collection_class = PurePostCollection


class PureCommentCollection(ModelCollection):
    model = Comment


class CommentCollection(MetaModelCollection):
    collection_class = PureCommentCollection


class PureLikeCollection(ModelCollection):
    model = Like


class LikeCollection(MetaModelCollection):
    collection_class = PureLikeCollection


class PureRepostCollection(ModelCollection):
    model = Repost


class RepostCollection(MetaModelCollection):
    collection_class = PureRepostCollection


class PureTagCollection(ModelCollection):
    model = Tag


class TagCollection(ModelCollection):
    collection_class = PureTagCollection


class PureChannelCollection(ModelCollection):
    model = Channel


class ChannelCollection(MetaModelCollection):
    collection_class = PureChannelCollection
