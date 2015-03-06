import vinepy


def main():
    vine = vinepy.API(username='something@yourmail.com', password='password')
    # You can create a vine account 
    # user = vine.signup(username='Your Name', email='something@yourmail.com', password='password')
    tag_timeline = vine.get_tag_timeline(tag_name='LNV')

    for post in tag_timeline:
        print(post.shareUrl)

if __name__ == '__main__':
    main()
