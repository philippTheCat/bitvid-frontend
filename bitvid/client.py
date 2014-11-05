# -*- coding: utf-8 -*-

import requests
import json

from .utils import gluequery


class HttpClient(object):
    def __init__(self, endpoint=None, clientbase=requests, debug=False):
        """Creates a new :class:`HttpClient` object.

        :param endpoint: The default endpoint to send requests to. This is
                         optional and can also be provided in :meth:`request`
                         or the shorthand methods.
        :param clientbase: The base library which will execute the requests.
                           By default, this is set to the `requests` library.
                           For testing, it's advised to use Flask's request
                           testing module.
        :param debug: Set this to ``True`` to activate the debug mode.
                      In debug mode, all the requests and responses will
                      be printed.
        """
        self.endpoint = endpoint
        self.client = clientbase
        self.testing = clientbase != requests
        self.authtoken = None
        self.debug = debug

    def _parse_json(self, response):
        if self.testing:
            # Flask test app
            return json.loads(response.data)
        else:
            return response.json()

    def request(self, method, path, data=None, query='', headers=None,
                endpoint=None, parse_json=True):
        """Executes a HTTP request to the endpoint.

        :param method: The HTTP method from the `requests` library
        :param path: The path to append to the endpoint. This can be a
                     'precompiled' path or a list with the parts. It should
                     start with a forward slash.
        :param query: The query to append to the url. This can also be a
                      'precompiled' query or a list of the query parts.
        :param data: The body of the request.
        :param headers: The request headers as `dict`. By default this will
                        have a ``'Content-Type'`` set to ``'application/json'``.
                        If the `authtoken` is present, this will be set in
                        the headers as ``'token'``
        :param endpoint: Optional override of the endpoint.
        :param parse_json: When ``True``, the response text will automatically
                           be parsed as JSON. Set this to ``False`` if you
                           also require different response data such as
                           status codes.
        """
        if not isinstance(path, basestring):
            path = '/'.join(path)
        if isinstance(query, dict):
            query = '?' + '&'.join(gluequery(query))
        url = '{endpoint}{path}{query}'.format(
            endpoint=endpoint if endpoint else self.endpoint,
            path=path,
            query=query
        )

        if headers is None:
            headers = {}
        if 'Content-Type' not in headers.keys():
            headers['Content-Type'] = 'application/json'
        if self.authtoken:
            headers['token'] = self.authtoken

        json_data = json.dumps(data) if isinstance(data, dict) else data

        if self.debug:
            print('\n\033[32m'
                  'Executing {method} request:\n'
                  '    URL: {url}\n'
                  '    headers: {headers}\n'
                  '    data: {data}'.format(method=method.func_name.upper(),
                                              url=url,
                                              headers=headers,
                                              data=data))

        response = method(url, data=json_data, headers=headers)
        status_code = response.status if self.testing else response.status_code

        reason = requests.codes[status_code]
        if 400 <= status_code < 500:
            http_error_msg = '%s Client Error: %s' % (status_code, reason)
            ex = Exception(http_error_msg)
            ex.data = self._parse_json(response)

        elif 500 <= status_code < 600:
            http_error_msg = '%s Server Error: %s' % (status_code, reason)
            ex = Exception(http_error_msg)
            ex.data = self._parse_json(response)

        json_response = None
        if parse_json:
            json_response = self._parse_json(response)

        if self.debug:
            if json_response is None:
                json_response = self._parse_json(response)
            print('\033[93m'
                  'Response [{status_code}] of {method} request:\n'
                  '    {response}'
                  '\033[0m\n'.format(status_code=response.status_code,
                                     method=method.func_name.upper(),
                                     response=json_response))

        if parse_json:
            return json_response
        return response

    def post(self, *args, **kwargs):
        """Shorthand to execute *POST* requests on the endpoint."""
        return self.request(self.client.post, *args, **kwargs)

    def get(self, *args, **kwargs):
        """Shorthand to execute *GET* requests on the endpoint."""
        return self.request(self.client.get, *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Shorthand to execute *DELETE* requests on the endpoint."""
        return self.request(self.client.delete, *args, **kwargs)

    def put(self, *args, **kwargs):
        """Shorthand to execute *PUT* requests on the endpoint."""
        return self.request(self.client.put, *args, **kwargs)


class BitvidClient(HttpClient):
    def __init__(self, *args, **kwargs):
        super(BitvidClient, self).__init__(*args, **kwargs)
        self.userid = None

    def get_user(self, userid='current'):
        return self.get(['/user', userid])

    def authenticate(self, email, password):
        print("Authenticating {email}:{password}".format(
            email=email, password=password))

        data = {'email': email, 'password': password}
        response = self.post('/auth/', data, parse_json=False)
        print("Authentication data", self._parse_json(response))
        if response.status_code != 200:
            return self._parse_json(response)
        else:
            self.authtoken = self._parse_json(response)['token']
            return self._parse_json(response)

    def register(self, email, password):
        print("Registering {email}:{password}".format(
            email=email, password=password))

        data = {'email': email, 'password': password}
        data = self.post('/user/', data, parse_json=False)
        if data.status_code != 200:
            return self._parse_json(data)
        else:
            self.userid = self._parse_json(data)['id']
            print(self.userid)
            return self._parse_json(data)

    def comment(self, title, content, video, parent=None):
        print("Commenting: parent={parent} video={video} {title}:\n"
              "{content}".format(title=title, content=content, video=video,
                                 parent=parent))
        data = {'title': title, 'content': content, 'parent': parent}
        return self.post(['/video', video, 'comments'], data)

    def getComment(self, token):
        print("Getting comment with token: " + token)
        return self.get(['/comment', token])

    def _getVideoToken(self, title, description):
        print("Getting video token: {title}\n{description}".format(
            title=title, description=description))
        data = {'title': title, 'description': description}
        return self.post('/video/', data)

    def getCommentsForVideo(self, videotoken):
        print("Getting comments for video: " + videotoken)
        response = self.get(['/video', videotoken, 'comments'])
        return response['comments']

    def unregister(self, email, password):
        print("Unregistering user: " + email)
        return self.delete('/user/', {'email': email, 'password': password})

    def changePassword(self, email, oldpass, newpass):
        print('Changing password for user: ' + email)
        data = {'email': email, 'password': oldpass, 'newpassword': newpass}
        return self.put('/user/', data)

    def deleteComment(self, commentToken):
        print("Deleting comment " + commentToken)
        return self.delete(['/comment', commentToken])

    def updateComment(self, token, title, content):
        print("Updating comment " + token)
        data = {'title': title, 'content': content}
        return self.put(['/comment', token], data)

    def getVideo(self, token):
        return self.get(['/video', token])

    def updateVideo(self, token, title, description):
        data = {'title': title, 'description': description}
        return self.post(['/video', token], data)

    def uploadVideo(self, token, videoFile):
        ext = videoFile.filename.split(".")[-1]
        conttype = "video/"+ext
        headers = {"Content-Type": conttype}
        return self.put("/video/"+token, videoFile.read(), headers=headers)

    def search(self, query, page = 0):
        return self.get('/search', query=dict(q=query,page=page))

    def deleteVideo(self, token):
        return self.delete(['/video', token])
