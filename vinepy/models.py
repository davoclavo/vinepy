import json
from datetime import datetime

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
        self.get_collection().__iter__()

    def next(self):
        return self.get_collection().next()

    def get_collection(self):
        return self.get(self.model_key, [])


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

    def connect_api(self, api):
        self.api = api
        if('key' in self.keys()):
            self.api.authenticate(self)

    def followers(self, **kwargs):
        return self.api.get_followers(user_id=self.id, **kwargs)


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


# mention or hashtag in comment or title
class Entity(Model):
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
