import requests
import json


class HTTPClient:

    def __init__(self, baseurl, clientBase=requests):
        self.baseurl = baseurl
        self.authtoken = ""
        self.userid = -1
        self.request = clientBase
        self.testing = clientBase != requests

    def _json(self, response):
        if self.testing:  # flask test app
            return json.loads(response.data)
        else:
            return response.json()

    def _request(self, op, url, data, headers=None):
        if headers == None:
            headers = {}

        if "Content-Type" not in headers.keys():
            headers["Content-Type"] = "application/json"

        if self.authtoken:
            headers["token"] = self.authtoken

        fullurl = self.baseurl + url
        print fullurl

        dataencoded = None
        if isinstance(data,dict):
            dataencoded = json.dumps(data)
        else:
            dataencoded = data

        val = op(fullurl, data=dataencoded, headers=headers)
        responsecode = None
        if self.testing:  # flask test app
            responsecode = val.status
        else:
            responsecode = val.status_code

        reason = requests.status_codes.codes[responsecode]
        if 400 <= responsecode < 500:
            http_error_msg = '%s Client Error: %s' % (responsecode, reason)
            ex = Exception(http_error_msg)
            ex.data = self._json(val)

        elif 500 <= responsecode < 600:
            http_error_msg = '%s Server Error: %s' % (responsecode, reason)
            ex = Exception(http_error_msg)
            ex.data = self._json(val)

        return val

    def _post(self, url, data={}):
        val = self._request(self.request.post, url, data)
        return val

    def _get(self, url, data={}):
        val = self._request(self.request.get, url, data)
        return val

    def _delete(self, url, data={}):
        val = self._request(self.request.delete, url, data)
        return val

    def _put(self, url, data={}, headers=None):
        val = self._request(self.request.put, url, data, headers=headers)
        return val

    def getUser(self,userid="current"):
        return self._json(self._get("/user/"+userid))

    def authenticate(self, email, password):
        print "authenticating {email}:{password}".format(email=email, password=password)
        logindata = {
            "email": email,
            "password": password
        }
        authdata = self._post("/auth/", logindata)
        print "authdata", self._json(authdata)
        if authdata.status_code is not 200:
            return self._json(authdata)
        else:
            self.authtoken = self._json(authdata)["token"]
            return self._json(authdata)


    def register(self, email, password):
        print "registrating {email}:{password}".format(email=email, password=password)
        registerdata = {
            "email": email,
            "password": password
        }
        registerdata = self._post("/user/", registerdata)
        if registerdata.status_code is not 200:
            return self._json(registerdata)
        else:
            self.userid = self._json(registerdata)["id"]
            print self.userid
            return self._json(registerdata)

    def comment(self, title, content, video, parent=None):
        print "commenting: parent={parent} video={video} {title}:\n{content}".format(title=title, content=content, video=video, parent=parent)

        commentdata = {
            "title": title,
            "content": content,
            "parent": parent
        }

        returndata = self._post(
            "/video/{videoToken}/comments".format(videoToken=video), commentdata)

        print self._json(returndata)
        return self._json(returndata)

    def getComment(self, token):
        print "getting comment with token: " + token

        returndata = self._get("/comment/%s" % token)
        print "rawreturndata", returndata.data
        print self._json(returndata)
        return self._json(returndata)

    def _getVideoToken(self, title, description):
        print "getting Video Token: {title}\n{description}".format(title=title, description=description)

        videoTokenData = {
            "title": title,
            "description": description
        }

        returndata = self._post("/video/", videoTokenData)

        return self._json(returndata)

    def getCommentsForVideo(self, videotoken):
        print "getting comments for video", videotoken

        returndata = self._get(
            "/video/{videoToken}/comments".format(videoToken=videotoken))

        return self._json(returndata)["comments"]

    def unregister(self, email, password):
        print "unregistering user", email
        returndata = self._delete(
            "/user/", {"email": email, "password": password})
        return returndata

    def changePassword(self, email, oldpass, newpass):
        print "changing password for user", email
        updatedata = {"email": email,
                      "password": oldpass,
                      "newpassword": newpass}
        returndata = self._put("/user/", updatedata)

        return self._json(returndata)

    def deleteComment(self, commentToken):
        print "deleting comment ", commentToken
        returndata = self._delete("/comment/" + commentToken)
        return self._json(returndata)

    def updateComment(self, token, title, content):
        print "updating comment ", token
        commentdata = {
            "title": title,
            "content": content
        }

        returndata = self._put("/comment/"+token, commentdata)

        return self._json(returndata)

    def getVideo(self, token):
        return self._json(self._get("/video/"+token))

    def updateVideo(self, token, title, description):
        updateData = {
            "title": title,
            "description": description
        }
        returndata = self._post("/video/"+token, updateData)
        return self._json(returndata)

    def uploadVideo(self, token, videoFile):
        ext = videoFile.filename.split(".")[-1]
        conttype = "video/"+ext
        headers = {
            "Content-Type": conttype
        }
        returndata = self._put("/video/"+token, videoFile.read(), headers=headers)
        return self._json(returndata)

    def search(self, searchquery):
        returndata = self._get("/search?q="+searchquery)
        return self._json(returndata)

    def deleteVideo(self, token):
        returndata = self._delete("/video/"+token)
        return self._json(returndata)