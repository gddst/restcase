"""
"""
from unittest.result import TestResult

from .testcase import RESTCase
from .client import RESTClient
from .httputil import HTTP_HEADER
from .httputil import MEDIA_TYPE
from .httputil import REQUEST_SPEC
from .testcase import TEST_CASE_SPEC


__all__ = [
]

def run_test(testcase_spec, ext_validator=None, setup=None, teardown=None):

    if setup:
        setup()

    try:
        RESTCase(testcase_spec, ext_validator, methodName='run_test').run_test()
    finally:
        if teardown:
            teardown()
    
    # If invoke testcase by "run", all the assertion exception will be intercepted
    # by unittest framework. To make the outer framework (Say StromTest) being 
    # able to catch the assertion exception, we should directly invoke the test 
    # method like above. 
    #test_result=TestResult()
    #RESTCase(testcase_spec).run(test_result)
    #print test_result


def request(testcase_spec):
    request_obj=RESTCase.Get_request_obj(testcase_spec)
    with RESTClient() as client:
        responseInfo=client.request(request_obj)
    return responseInfo


def workflow():
    """ToDo
    """
    pass
