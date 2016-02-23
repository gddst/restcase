import json
from unittest import TestCase
import unittest
import urllib

#from jsonpath_rw import jsonpath, parse
#from jsonpath_rw.jsonpath import Fields

from restcase.client import RESTClient
from restcase.httputil import REQUEST_SPEC, HTTP_HEADER, MEDIA_TYPE


class RESTCase(TestCase):
    
    default_validator="Status"
    
    def __init__(self, testcase_spec, ext_validator=None, methodName="no_test"):
        super(RESTCase, self).__init__(methodName=methodName)
        self.__testcase_spec=testcase_spec
        self.__ext_validator=ext_validator

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def no_test(self):
        pass
    
    #@unittest.skip("")
    def run_test(self):

        request_obj= RESTCase.Get_request_obj(self.__testcase_spec)
        with RESTClient() as client:
            response_info=client.request(request_obj)

        expectation_list=self.__testcase_spec.get(TEST_CASE_SPEC.EXPECTATION)

        if not expectation_list:
            #The default expectation is a 200 response code.
            expectation_list=[{"validator":RESTCase.default_validator}]

        for expect in expectation_list:                
            validator_name=expect.get("validator")
            args=expect.get('args',{})
            if validator_name:
                try:
                    validator=getattr(self, "assert"+validator_name)
                except AttributeError,e:
                    if self.__ext_validator:
                        validator=getattr(self.__ext_validator, "assert"+validator_name)
                    else:
                        raise e
                validator(response_info,**args)

            
    @staticmethod
    def Get_request_obj(testcase_spec):
        request_obj=testcase_spec.get(TEST_CASE_SPEC.INPUT)
        
        req_paras=request_obj.get(REQUEST_SPEC.REQ_PARAS, {})
        content_type=request_obj.get(REQUEST_SPEC.HEADERS,{}).get(HTTP_HEADER.CONTENT_TYPE)
        
        request_obj[REQUEST_SPEC.QUERY_PARAMS]= request_obj.get(REQUEST_SPEC.URL_PARAS, {})

        if content_type==MEDIA_TYPE.X_WWW_FORM_URLENCODED and req_paras:
            request_obj[REQUEST_SPEC.BODY]= urllib.urlencode(req_paras,True)
        else:
            request_obj[REQUEST_SPEC.QUERY_PARAMS].update(req_paras)
    
        if REQUEST_SPEC.REQ_PARAS in request_obj:
            del request_obj[REQUEST_SPEC.REQ_PARAS]
        if REQUEST_SPEC.URL_PARAS in request_obj:
            del request_obj[REQUEST_SPEC.URL_PARAS]
        
        return request_obj

    #
    #    Assertion Methods
    #

    def assertStatus(self, response, status=200):
        """

        :param response:
        :param status:
        :return:
        """
        self.assertEqual(response.status, status)

    def assertHeader(self, response, header={}):
        """

        :param response:
        :param header:
        :return:
        """
        name=header.items()[0][0]
        exp_value=header.items()[0][1]
        self.assertEqual(response.headers.get(name), exp_value)

    '''
    Json Assertion Methods
    '''
    def assertJsonKeyEqual(self, response, key_path=[], exp_value=None):
        '''
        '''
        body_json=json.loads(response.body)

        real_value=getJsonKey(body_json, key_path)
        self.assertEqual(real_value, exp_value)

    """
    def assertJsonFieldEqual(self, response, json_path=None, exp_value=None):
        '''
        '''
        body_json=json.loads(response.body)
        print body_json
        jsonpath_expr=parse(json_path)
        
        #
        #jsonpath_expr=Fields(json_path)
        
        print jsonpath_expr.__class__
        result=jsonpath_expr.find(body_json)
        print result
        real_value=result[0].value
        self.assertEqual(real_value, exp_value)
    """

    def assertJsonKeyNotEqual(self, response, key_path=[], exp_value=None):
        """
        """
        body_json=json.loads(response.body)

        real_value=getJsonKey(body_json, key_path)
        self.assertNotEqual(real_value, exp_value)

    def assertJsonKeyIn(self, response, key_path):
        body_json=json.loads(response.body)
        getJsonKey(body_json, key_path)

    def assertJsonKeyNotIn(self, response, key_path):
        body_json=json.loads(response.body)
        with self.assertRaises(KeyError):
            getJsonKey(body_json, key_path)


def getJsonKey(json_obj, key_path):
    cur_entry=json_obj
    for key in key_path:
        cur_entry=cur_entry[key]
    return cur_entry


class TestCaseSpec(object):
    
    @property
    def DESCRIPTION(self):
        return 'description'
        
    @property
    def INPUT(self):
        return 'input'
    
    @property
    def EXPECTATION(self):
        return 'expectation'
    
    @property
    def SETUP(self):
        return 'setup'
    
    @property
    def TEARDOWN(self):
        return 'teardown'

TEST_CASE_SPEC= TestCaseSpec()

__all__= [
    TEST_CASE_SPEC,
    RESTCase
]

if __name__=="__main__":
    print None==None
    a={None:'a'}
    print a.get(None)