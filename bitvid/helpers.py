# -*- coding: utf-8 -*-

from pprint import pprint
from math import ceil
from flask import flash, g

from bitvid import app


def video_query(query, page = 0):
    videos = g.api.search.get(params={'q': query, 'page': page})
    pages = int(ceil(videos.num / 10.0))
    return pages, videos.hits
