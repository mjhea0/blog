#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Kyle W. Purdon'
SITENAME = u'Kyle W. Purdon'
HIDE_SITENAME = True
SITEURL = 'http://kylepurdon.com/blog'

MENUITEMS = (('Home', 'http://kylepurdon.com'),
             ('Blog', 'http://kylepurdon.com/blog'),
             ('About', 'http://kylepurdon.com/about.html'))

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_TAGS_ON_SIDEBAR = False
DISPLAY_CATEGORIES_ON_SIDEBAR = True

THEME = '../pelican-bootstrap3'
BOOTSTRAP_THEME = 'flatly'
USE_PAGER = True

PATH = 'content'
STATIC_PATHS = ['images']

TIMEZONE = 'America/Denver'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
    ('Twitter', 'https://twitter.com/PurdonKyle'),
    ('Github', 'https://github.com/kpurdon'),
    ('Google+', 'https://plus.google.com/u/0/+KylePurdon'),
    ('Reddit', 'http://www.reddit.com/user/kpurdon/'),
    ('LinkedIn', 'https://www.linkedin.com/in/kylepurdon'),
)

DEFAULT_PAGINATION = 5
