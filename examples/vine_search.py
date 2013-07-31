import sys, os
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))


import vinepy

def main():
    vine = vinepy.API(username='elgo@suremail.info', password='12345678')
    # user = vine.signup(username='Elgo', email='elgo@suremail.info', password='12345678')
    tag_timeline = vine.get_tag_timeline(tag_name='LNV')

    for post in tag_timeline:
        print post.shareUrl

if __name__ == '__main__':
    main()
