# -*- coding: utf-8 -*-

from pprint import pprint
from math import ceil
from flask import flash, g

from bitvid import app


def video_query(query, page = 0):
    data = g.client.search(query, page = page)
    pprint(data, indent=4)
    try:
        if "message" in data.keys():
            print "data", data
            flash("could not load videos")
            return {}
    except Exception as ex:
        print ex
        return {}

    pages = int(ceil(data["num"]/10.0))

    return pages, data["hits"] #videos_from_json(data)

