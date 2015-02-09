import sys
import os
import vinepy


def main():
    vine = vinepy.API(username='bobtesty@suremail.info', password='password')
    # user = vine.signup(username='Elgo', email='elgo@suremail.info', password='12345678')
    tag_timeline = vine.get_tag_timeline(tag_name='LNV')

    for post in tag_timeline:
        print post.shareUrl

if __name__ == '__main__':
    main()
