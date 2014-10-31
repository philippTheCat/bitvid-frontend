# -*- coding: utf-8 -*-

def gluequery(query):
    try:
        for key, value in query.iteritems():
            yield '%s=%s' % (key, value)
    except AttributeError:
        # query did not have an `iteritems()` method
        yield query
