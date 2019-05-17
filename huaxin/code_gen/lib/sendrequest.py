"""
Created on 2011-8-19

@author: Chester.Qian
"""
import cookielib
import requests
import urllib2
import urllib
import MultipartPostHandler

def sendGetRequest(url, headers=None, **kwargs):
    """
    About Basic Authentication:
        http://docs.python-requests.org/en/latest/user/authentication/#basic-authentication

    For some web services that require authentication accept HTTP Basic Auth,
    caller can pass to kwargs in below format:
    e.g. auth=('<user>', '<password>')
    """
    print url
    if not kwargs:
        handlers = [
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
            ]

        opener = urllib2.build_opener(*handlers)
        request = urllib2.Request(url)

        if headers:
            for k in headers.keys():
                request.add_header(k, headers[k])
        response = opener.open(request)
    else:
        response = requests.get(url, **kwargs)

    return response

def sendPostRequest(url, Parameter, headers, **kwargs):
    """
    About Basic Authentication:
        http://docs.python-requests.org/en/latest/user/authentication/#basic-authentication

    For some web services that require authentication accept HTTP Basic Auth,
    caller can pass to kwargs in below format:
    e.g. auth=('<user>', '<password>')
    """
    if 'auth' in kwargs:
        # Parameter: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        if Parameter:
            response = requests.post(url, data=Parameter, **kwargs)
    else:
        for k in Parameter.keys():
            if type(Parameter[k]) == unicode:
                Parameter.update({k:Parameter[k].encode('utf8')})

        cookies, response = sendPOST(url, urllib.urlencode(Parameter), headers)

    return response

def sendMultipartPostRequest(Url,Parameter):
    print Url, Parameter
    cookies = cookielib.CookieJar()
    MultipartPost_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                MultipartPostHandler.MultipartPostHandler)

    resp = MultipartPost_opener.open(Url, Parameter)

def sendPOST(url, data, headers):
    cookies = cookielib.CookieJar()

    handlers = [
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(cookies)
    ]

    opener = urllib2.build_opener(*handlers)

    request = urllib2.Request(url, data, headers)

    try:
        response = opener.open(request)
    except urllib2.HTTPError, e:
        return cookies, None

    return cookies, response

def dumpCookies(cookies):
    cookie_string = ""

    for cookie in cookies:
        if type(cookies) is list:
            cookie_string += cookie['name'] + "=" + cookie['value'] + ";"
        else: 
            "type(cookies) is instance"
            cookie_string += cookie.name + "=" + cookie.value + ";"

    return cookie_string