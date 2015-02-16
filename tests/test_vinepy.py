import sys
import os

import vcr
import vinepy

from nose2.compat import unittest


my_vcr = vcr.VCR(
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
    # record_mode = 'all' # Re-record cassettes
)


class TestAPI(unittest.TestCase):

    @my_vcr.use_cassette('login.yml')
    @classmethod
    def setUp(cls):
        cls.vine_name = 'Bob Testy'
        cls.vine_email = 'bobtesty@suremail.info'
        cls.vine_password = 'password'
        cls.api = vinepy.API(
            username=cls.vine_email, password=cls.vine_password)

    @my_vcr.use_cassette('signup.yml')
    def test_signup(self):
        api = vinepy.API().signup(
            username=self.vine_name, email=self.vine_email, password=self.vine_password)
        self.assertEqual(api.username, self.vine_name)

    @my_vcr.use_cassette('tag_timeline.yml')
    def test_get_tag_timeline(self):
        timeline = self.api.get_tag_timeline(tag_name='LNV')
        assert(timeline._attrs)

    @my_vcr.use_cassette('vm_friends_inbox.yml')
    def test_get_friends_inbox(self):
        conversations = self.api.get_conversations(
            user_id=self.api.user.userId)
        assert(conversations._attrs)

    @my_vcr.use_cassette('get_post.yml')
    def test_get_post(self):
        post_id = 1167619641938518016
        # Retrieves PostCollection
        post = self.api.get_post(post_id=post_id)[0]
        self.assertEqual(post.id, post_id)
        self.assertEqual(
            post.name, 'In-N-Out vs. Shake Shack: The Ultimate Battle')

    def test_custom_device_token(self):
        with my_vcr.use_cassette('login-custom-device-token.yml') as cassette:
            custom_device_token = 'a3352a79c3e29283a03a2e6eb89587648f5b2a291c709708816ec768d058ea45'
            api = vinepy.API(
                username=self.vine_email, password=self.vine_password, device_token=custom_device_token)
            self.assertIn(custom_device_token, cassette.requests[0].body)
            self.assertEqual(api.username, self.vine_email)

    def test_user_notifications(self):
        api = vinepy.API(username=self.vine_email, password=self.vine_password)
        user_id = 948731399408640000

        with my_vcr.use_cassette('unfollow_notifications.yml') as cassette:
            api.unfollow_notifications(user_id=user_id)
            user = api.get_user(user_id=user_id)
            self.assertTrue(user.is_following())
            self.assertFalse(user.is_notifying())

        with my_vcr.use_cassette('follow_notifications.yml') as cassette:
            api.follow_notifications(user_id=user_id)
            user = api.get_user(user_id=user_id)
            self.assertTrue(user.is_following())
            self.assertTrue(user.is_notifying())


class TestModel(unittest.TestCase):
    # Model method tests

    def test_model_from_json(self):
        mock_json = {'id': 1,
                     'from_json': 'something'
                     }
        model = vinepy.Model.from_json(mock_json)
        self.assertEqual(model['id'], mock_json['id'])
        # Does not replace an existing key
        self.assertNotEqual(model.from_json, mock_json['from_json'])

        # classname + 'Id' replaces 'id' key
        mock_json['modelId'] = 2
        model = vinepy.Model.from_json(mock_json)
        self.assertEqual(model.id, mock_json['modelId'])

    def test_model_from_id(self):
        _id = 123
        model = vinepy.Model.from_id(_id)
        self.assertEqual(_id, model.id)

    def test_model_repr(self):
        # No name attribute sets it to <Unknown>
        _id = 123
        model = vinepy.Model.from_json({'id': _id})
        self.assertEqual(repr(model), "<Model [%s] '%s'>" % (_id, '<Unknown>'.encode('utf8')))

        # Unicode name (emojis)
        _description = u'Lmaoo\U0001f602'
        model = vinepy.Post.from_json({'id': _id, 'description': _description})
        self.assertEqual(repr(model), "<Post [%s] '%s'>" % (_id, _description.encode('utf8')))


class TestDecorator(unittest.TestCase):
    # Decorator tests

    def test_vine_json(self):
        pass

    def test_ensure_ownership(self):
        pass

    def test_chained(self):
        pass

    def test_inject_post(self):
        pass


class TestUtils(unittest.TestCase):
    short_id = 'OjunvOxTpZ5'
    long_id = 1167619641938518016

    def test_post_long_id(self):
        long_id = vinepy.post_long_id(self.short_id)
        self.assertEqual(self.long_id, long_id)

    def test_post_short_id(self):
        short_id = vinepy.post_short_id(self.long_id)
        self.assertEqual(self.short_id, short_id)
