#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "dc.hess@gmail.com"
SITEURL = "https://dchess.github.io"
SITENAME = "dchess"
SITETITLE = "D.C. Hess"
SITESUBTITLE = "Software Engineer"
SITEDESCRIPTION = "Code, code, and more code"
THEME = "themes/flex"
SITELOGO = "/images/profile.jpg"
FAVICON = "/images/favicon.ico"

STATIC_PATHS = ["images", "extra", "extra/CNAME"]

EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
    "extra/CNAME": {"path": "CNAME"},
}

CUSTOM_CSS = "static/custom.css"

DISQUS_SITENAME = "dchess-org"
PATH = "content"

TIMEZONE = "America/Los_Angeles"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MAIN_MENU = True
MENUITEMS = (("Projects", "/category/projects.html"),)

# Blogroll
LINKS = (
    (
        "resume",
        "https://drive.google.com/file/d/1O0-Le26SdL-DhDo2LsOQVWR5BAV4I17F/view",
    ),
)

# Social widget
SOCIAL = (
    ("github", "https://www.github.com/dchess"),
    ("twitter", "https://twitter.com/dc_hess"),
    ("linkedin", "https://www.linkedin.com/in/dchess"),
    ("envelope-o", "mailto:dc.hess@gmail.com"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PYGMENTS_STYLE = "monokai"

MARKUP = ("md", "ipynb")

from pelican_jupyter import markup as nb_markup

PLUGINS = [nb_markup]
IPYNB_MARKUP_USE_FIRST_CELL = True

IGNORE_FILES = [".ipynb_checkpoints"]