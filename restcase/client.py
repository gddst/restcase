"""
"""

import httplib
import ssl
import timeit
import urllib

from httputil import REQUEST_SPEC
from httputil import HTTP_METHOD

class RESTClient(object):

    def __init__(self):
        self.__conn = None

    def __connect(self, host, scheme='https', ca_certs=None):
        self.__host = host
        self.__scheme = scheme
        if scheme == 'https':
            context = ssl.create_default_context()
            if ca_certs:
                pass
            else:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

            self.__conn = httplib.HTTPSConnection(host, context=context)
        else:
            self.__conn = httplib.HTTPConnection(host)

            
    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print exc_type.__name__, ':', exc_value
            print exc_traceback
        elif self.__conn:
            self.__conn.close()
  
    
    def request(self, request_obj, verbose=False):

        if not self.__conn:
            self.__connect(request_obj.get(REQUEST_SPEC.HOST), request_obj.get(REQUEST_SPEC.SCHEME))

        http_method = request_obj.get(REQUEST_SPEC.METHOD, HTTP_METHOD.GET)
        path_query = RESTClient.__build_path_query(request_obj)
        body = request_obj.get(REQUEST_SPEC.BODY)
        
        req_stat = RESTClient.__get_url(request_obj)
        print http_method, req_stat
        
        
        headers = request_obj.get(REQUEST_SPEC.HEADERS, {})
        
        start_time = timeit.default_timer()
        self.__conn.request(http_method , path_query , body , headers)
        request_time = timeit.default_timer()
        
        response = self.__conn.getresponse()
        response_time = timeit.default_timer()
        
        class ARTResponse(object):
            pass
        response_info = ARTResponse()
        
        #deprecated
        response_info.data = response.read()
        response_info.body=response_info.data        
        
        end_time = timeit.default_timer()
        
        response_info.request_time = request_time - start_time
        response_info.response_time = response_time - request_time
        response_info.local_read_time = end_time - response_time        

        response_info.request_statement = req_stat
        response_info.status=response.status
        response_info.reason = response.reason        
        response_info.headers = { header[0]:header[1] for header in response.getheaders()}
        
        response_info.content_type = response.getheader('Content-Type', 'unknown!')
        response_info.content_length = response.getheader('Content-Length', 'unknown!')
        
        response_info.duration=end_time-start_time

        return response_info
        
    @staticmethod
    def __build_path_query(request_spec):
        query_string=""
        query = request_spec.get(REQUEST_SPEC.QUERY_PARAMS)
        if query:
            query_string = "?"+urllib.urlencode(query)
        return request_spec.get(REQUEST_SPEC.PATH, '') + query_string
    
    @staticmethod
    def __get_url(request_spec):
        return "{scheme}://{host}{path_query}".format(
            scheme=request_spec.get(REQUEST_SPEC.SCHEME),
            host=request_spec.get(REQUEST_SPEC.HOST),
            path_query=RESTClient.__build_path_query(request_spec)
        )

if __name__ == '__main__':
    pass
