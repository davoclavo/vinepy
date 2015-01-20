import sys, os
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))

import vcr
import vinepy
from nose.tools import *


my_vcr = vcr.VCR(
    cassette_library_dir = 'fixtures/cassettes',
    record_mode = 'once',
    match_on = ['uri', 'method'],
    # record_mode = 'all' # Re-record cassettes
)

class TestVinepy:
    @my_vcr.use_cassette('login.yml')
    @classmethod
    def setup_class(cls):
        cls.vine_name = 'Bob Testy'
        cls.vine_email = 'bobtesty@suremail.info'
        cls.vine_password = 'password'
        cls.api = vinepy.API(username=cls.vine_email, password=cls.vine_password)
 
    @classmethod
    def teardown_class(cls):
        pass


    @my_vcr.use_cassette('signup.yml')
    def test_signup(self):
        api = vinepy.API().signup(username=self.vine_name, email=self.vine_email, password=self.vine_password)
        assert_equals(api.username, self.vine_name)

    @my_vcr.use_cassette('tag_timeline.yml')
    def test_get_tag_timeline(self):
        timeline = self.api.get_tag_timeline(tag_name='LNV')
        assert(timeline._attrs)

    @my_vcr.use_cassette('get_post.yml')
    def test_get_post(self):
        post_id = 1167619641938518016

        # Retrieves PostCollection
        post = self.api.get_post(post_id=post_id)[0]
        assert_equals(post.id, post_id)
        assert_equals(post.name, 'In-N-Out vs. Shake Shack: The Ultimate Battle')
