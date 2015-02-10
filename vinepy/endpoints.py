from .models import *

PROTOCOL = 'https'
API_HOST = 'api.vineapp.com'
MEDIA_HOST = 'media.vineapp.com'

HEADERS = {
    'Host':              'api.vineapp.com',
    'Proxy-Connection':  'keep-alive',
    'Accept':            '*/*',
    'X-Vine-Client':     'ios/2.5.1',
    'Accept-Encoding':   'gzip, deflate',
    'Content-Type':      'application/x-www-form-urlencoded; charset=utf-8',
    'Accept-Language':   'en;q=1',
    'Connection':        'keep-alive',
    'User-Agent':        'iphone/172 (iPad; iOS 7.0.4; Scale/2.00)'
}


OPTIONAL_PARAMS = ['size', 'page', 'anchor']

ENDPOINTS = {

    # Auth
    'login': {
        'endpoint': 'users/authenticate',
        'request_type': 'post',
        'url_params': [],
        'required_params': ['username', 'password'],
        'optional_params': ['deviceToken'],
        'default_params': [],
        'model': User
    },
    'logout': {
        'endpoint': 'users/authenticate',
        'request_type': 'delete',
        'url_params': [],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'signup': {
        'endpoint': 'users',
        'request_type': 'post',
        'url_params': [],
        'required_params': ['email', 'password', 'username'],
        'optional_params': [],
        'default_params': [('authenticate', 1)],
        'model': User
    },

    # Profile
    'get_me': {
        'endpoint': 'users/me',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': [],
        'model': User
    },
    'get_user': {
        'endpoint': 'users/profiles/%s',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': User
    },
    'update_profile': {
        'endpoint': 'users/%s',
        'request_type': 'put',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': ['username', 'description', 'location', 'locale', 'email', 'private', 'phoneNumber', 'avatarUrl', 'profileBackground', 'acceptsOutOfNetworkConversations'],
        'model': None
    },
    'set_explicit': {
        'endpoint': 'users/%s/explicit',
        'request_type': 'post',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'unset_explicit': {
        'endpoint': 'users/%s/explicit',
        'request_type': 'delete',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },

    # User actions
    'follow': {
        'endpoint': 'users/%s/followers',
        'request_type': 'post',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': ['notify'], # notify=1 to follow notifications as well
        'model': None
    },
    'follow_notifications': {
        'endpoint': 'users/%s/followers/notifications',
        'request_type': 'post',
        'url_params': ['user_id'],
        'required_params': ['notify'],
        'optional_params': [],
        'default_params': [('notify', 1)],
        'model': None
    },
    'unfollow': {
        'endpoint': 'users/%s/followers',
        'request_type': 'delete',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'unfollow_notifications': {
        'endpoint': 'users/%s/followers/notifications',
        'request_type': 'delete',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'block': {
        'endpoint': 'users/%s/blocked/%s',
        'request_type': 'post',
        'url_params': ['from_user_id', 'to_user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'unblock': {
        'endpoint': 'users/%s/blocked/%s',
        'request_type': 'delete',
        'url_params': ['from_user_id', 'to_user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'get_pending_notifications_count': {
        'endpoint': 'users/%s/pendingNotificationsCount',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'get_notifications': {
        'endpoint': 'users/%s/notifications',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': NotificationCollection
    },

    # User lists
    'get_followers': {
        'endpoint': 'users/%s/followers',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': UserCollection
    },
    'get_following': {
        'endpoint': 'users/%s/following',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': [],
        'model': UserCollection
    },

    'get_conversations': {
        'endpoint': 'users/%s/conversations',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': ['inbox'],
        'model': ConversationCollection
    },


    'start_conversation': {
        'endpoint': 'conversations',
        'request_type': 'post',
        'json': True,
        'url_params': [],
        'required_params': ['created', 'locale', 'message', 'to'],
        'optional_params': [],
        'model': MessageCollection
    },

    'converse': {
        'endpoint': 'conversations/%s',
        'request_type': 'post',
        'json': True,
        'url_params': ['conversation_id'],
        'required_params': ['created', 'locale', 'message'],
        'optional_params': [],
        'model': MessageCollection
    },

    # Posts actions
    'like': {
        'endpoint': 'posts/%s/likes',
        'request_type': 'post',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': [],
        'model': Like
    },
    'unlike': {
        'endpoint': 'posts/%s/likes',
        'request_type': 'delete',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'comment': {
        'endpoint': 'posts/%s/comments',
        'request_type': 'post',
        'json': True,
        'url_params': ['post_id'],
        'required_params': ['comment', 'entities'],
        'optional_params': [],
        'model': Comment
    },
    'uncomment': {
        'endpoint': 'posts/%s/comments/%s',
        'request_type': 'delete',
        'url_params': ['post_id', 'comment_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'revine': {
        'endpoint': 'posts/%s/repost',
        'request_type': 'post',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': [],
        'model': Repost
    },
    'unrevine': {
        'endpoint': 'posts/%s/repost/%s',
        'request_type': 'delete',
        'url_params': ['post_id', 'revine_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'report': {
        'endpoint': 'posts/%s/complaints',
        'request_type': 'post',
        'url_params': [],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'post': {
        'endpoint': 'posts',
        'request_type': 'post',
        'json': True,
        'url_params': [],
        'required_params': ['videoUrl', 'thumbnailUrl', 'description', 'entities'],
        'optional_params': ['forsquareVenueId', 'venueName'],
        'default_params': [('channelId', '0')],
        'model': Post
    },
    'delete_post': {
        'endpoint': 'posts/%s',
        'request_type': 'delete',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': [],
        'model': None
    },
    'get_post_likes': {
        'endpoint': 'posts/%s/likes',
        'request_type': 'get',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': LikeCollection
    },
    'get_post_comments': {
        'endpoint': 'posts/%s/comments',
        'request_type': 'get',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': [],
        'model': CommentCollection
    },
    'get_post_reposts': {
        'endpoint': 'posts/%s/reposts',
        'request_type': 'get',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': [],
        'model': RepostCollection
    },


    # Timelines
    'get_post': {
        'endpoint': 'timelines/posts/%s',
        'request_type': 'get',
        'url_params': ['post_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_user_timeline': {
        'endpoint': 'timelines/users/%s',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_user_likes': {
        'endpoint': 'timelines/users/%s/likes',
        'request_type': 'get',
        'url_params': ['user_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_tag_timeline': {
        'endpoint': 'timelines/tags/%s',
        'request_type': 'get',
        'url_params': ['tag_name'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_graph_timeline': {
        'endpoint': 'timelines/graph',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_popular_timeline': {
        'endpoint': 'timelines/popular',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_trending_timeline': {
        'endpoint': 'timelines/trending',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_promoted_timeline': {
        'endpoint': 'timelines/promoted',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_channel_popular_timeline': {
        'endpoint': 'timelines/channels/%s/popular',
        'request_type': 'get',
        'url_params': ['channel_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_channel_recent_timeline': {
        'endpoint': 'timelines/channels/%s/recent',
        'request_type': 'get',
        'url_params': ['channel_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },
    'get_venue_timeline': {
        'endpoint': 'timelines/venues/%s',
        'request_type': 'get',
        'url_params': ['venue_id'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': PostCollection
    },

    # Tags
    'get_trending_tags': {
        'endpoint': 'tags/trending',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': [],
        'model': TagCollection
    },

    # Channels
    'get_featured_channels': {
        'endpoint': 'channels/featured',
        'request_type': 'get',
        'url_params': [],
        'required_params': [],
        'optional_params': [],
        'model': ChannelCollection
    },

    # Search
    'search_tags': {
        'endpoint': 'tags/search/%s',
        'request_type': 'get',
        'url_params': ['tag_name'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': TagCollection
    },
    'search_users': {
        'endpoint': 'users/search/%s',
        'request_type': 'get',
        'url_params': ['user_name'],
        'required_params': [],
        'optional_params': OPTIONAL_PARAMS,
        'model': UserCollection
    },

    # Upload Media
    'upload_avatar': {
        'host': MEDIA_HOST,
        'endpoint': 'upload/avatars/1.3.1.jpg',
        'request_type': 'put',
        'url_params': [],
        'required_params': ['filename'],
        'optional_params': [],
        'model': None
    },
    'upload_thumb': {
        'host': MEDIA_HOST,
        'endpoint': 'upload/thumbs/2.5.1.15482401929932289311.mp4.jpg?private=1',
        'request_type': 'put',
        'url_params': [],
        'required_params': ['filename'],
        'optional_params': [],
        'model': None
    },
    'upload_video': {
        'host': MEDIA_HOST,
        'endpoint': 'upload/videos/2.5.1.15482401929932289311.mp4?private=1',
        'request_type': 'put',
        'url_params': [],
        'required_params': ['filename'],
        'optional_params': [],
        'model': None
    },
}
