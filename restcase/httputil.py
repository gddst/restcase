"""
"""

class _RequestSpec(object):
    SCHEME = 'scheme'
    METHOD = 'method'
    HOST = 'host'
    PATH = 'path'
    URL_PARAS = 'url_paras'
    REQ_PARAS = 'req_paras'
    HEADERS = 'headers'
    BODY = 'body'
    QUERY_PARAMS='query_params'

class _HttpMethod(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

class _HttpHeader(object):

    @property
    def CONTENT_TYPE(self):
        return 'Content-Type'

class _MediaType():
    
    @property
    def X_WWW_FORM_URLENCODED(self):
        return 'application/x-www-form-urlencoded'

REQUEST_SPEC = _RequestSpec()
HTTP_METHOD = _HttpMethod()
HTTP_HEADER = _HttpHeader()
MEDIA_TYPE = _MediaType()

__all__=[
    REQUEST_SPEC,
    HTTP_METHOD,
    HTTP_HEADER,
    MEDIA_TYPE
]
