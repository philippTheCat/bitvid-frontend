# -*- coding: utf-8 -*-

from pprint import pprint

from flask import flash, g

from bitvid import app


def video_url(token, height, extension):
    """Creates a URL for a video.

    Height probably relates to the quality of the video,
    e.g. 720p or 1080p.

    .. note:: This does not verify the existence of a video.

    :param token: Unique identifier of a video
    :param height: Options unclear
    :param extension: Options unclear
    """
    return "{host}/videos/{token}_{height}.{ext}".format(
        host=app.config['HOST'], token=token, height=height, ext=extension)


def video_query(query):
    data = g.client.search(query)
    pprint(data, indent=4)
    try:
        if "message" in data.keys():
            print "data", data
            flash("could not load videos")
            return {}
    except Exception as ex:
        print ex

    return videos_from_json(data)


def videos_from_json(json):
    try:
        if 'message' in json.keys():
            flash("Could not load any videos.")
            return {}
    except:
        pass

    results = []
    for video in json:
        videos = {}
        videomedias = g.client.getVideo(str(video["token"]))
        if "message" in videomedias.keys():
            pass
        else:
            pprint(videomedias, indent=4)
            for videomedia in videomedias["videos"]:
                if videomedia["codec"] not in videos.keys() or \
                                videomedia["height"] > \
                                videos[videomedia["codec"]]["height"]:
                    print(videomedia["codec"])
                    videomedia["path"] = video_url(video["token"],
                                                   videomedia["height"],
                                                   videomedia["codec"])
                    videos[videomedia["codec"]] = videomedia

        video["medias"] = videos
        results.append(video)

    pprint(results, indent=4)
    return results
