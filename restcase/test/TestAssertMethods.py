'''
Created on Dec 27, 2015

@author: gddst
'''
import json
import unittest

#from jsonpath_rw.jsonpath import Fields

from restcase.testcase import RESTCase


class TestRequest(unittest.TestCase):

    tc=RESTCase(None, methodName='no_test')

    '''
    Test of assertStatus
    '''

    def Test_AssertStatus_True(self):
        response_info=MockResponse(status=200)
        self.tc.assertStatus(response_info, status=200)

    def Test_AssertStatus_False(self):
        response_info=MockResponse(status=200)
        with self.tc.assertRaises(AssertionError):
            self.tc.assertStatus(response_info, status=201)

    '''
    Test of assertHeader
    '''

    def Test_AssertHeader_True(self):
        response_info=MockResponse(headers={'foo':'bar'})
        self.tc.assertHeader(response_info, header={'foo':'bar'})

    def Test_AssertHeader_False(self):
        response_info=MockResponse(headers={'foo':'bar'})
        with self.tc.assertRaises(AssertionError):
            self.tc.assertHeader(response_info, header={'foo':'xxx'})
    '''
    Test of assertJsonKeyEqual
    '''
    def Test_assertJsonKeyEqual_True_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value='bar')

    def Test_assertJsonKeyEqual_False_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value='xxx')

    def Test_assertJsonKeyEqual_True_depth_two(self):
        response=MockResponse(body=json.dumps({'foo':{'bar':'value'}}))
        self.tc.assertJsonKeyEqual(response,key_path=['foo','bar'],exp_value='value')

    def Test_assertJsonKeyEqual_False_depth_two(self):
        response=MockResponse(body=json.dumps({'foo':{'bar':'value'}}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyEqual(response,key_path=['foo','bar'],exp_value='xxx')

    def Test_assertJsonKeyEqual_True_bool(self):
        response=MockResponse(body=json.dumps({'foo':True}))
        self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value=True)

    def Test_assertJsonKeyEqual_False_bool(self):
        response=MockResponse(body=json.dumps({'foo':True}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value=False)

    def Test_assertJsonKeyEqual_True_int(self):
        response=MockResponse(body=json.dumps({'foo':0}))
        self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value=0)

    def Test_assertJsonKeyEqual_False_int(self):
        response=MockResponse(body=json.dumps({'foo':0}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value=1)
            
    def Test_assertJsonKeyEqual_True_list(self):
        response=MockResponse(body=json.dumps({'foo':['bar','baz']}))
        self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value=['bar','baz'])

    def Test_assertJsonKeyEqual_False_list(self):
        response=MockResponse(body=json.dumps({'foo':['bar','baz']}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyEqual(response,key_path=['foo'],exp_value=['bar','bax'])
    '''
    Test of assertJsonKeyNotEqual
    '''
    def Test_assertJsonKeyNotEqual_True_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        self.tc.assertJsonKeyNotEqual(response,key_path=['foo'],exp_value='xxx')

    def Test_assertJsonKeyNotEqual_False_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyNotEqual(response,key_path=['foo'],exp_value='bar')

    '''
    Test of assertJsonKeyIn
    '''
    def Test_assertJsonKeyIn_True_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        self.tc.assertJsonKeyIn(response,('foo',))

    def Test_assertJsonKeyIn_True_depth_two(self):
        response=MockResponse(body=json.dumps({'foo':{'bar':'xxx'}}))
        self.tc.assertJsonKeyIn(response,('foo','bar'))

    def Test_assertJsonKeyIn_False(self):
        response=MockResponse(body=json.dumps({'bar':'foo'}))
        with self.tc.assertRaises(KeyError):
            self.tc.assertJsonKeyIn(response,('foo',))

    '''
    Test of assertJsonKeyNotIn
    '''
    def Test_assertJsonKeyNotIn_True_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        self.tc.assertJsonKeyNotIn(response,('xxx',))

    def Test_assertJsonKeyNotIn_True_depth_two(self):
        response=MockResponse(body=json.dumps({'foo':{'bar':'xxx'}}))
        self.tc.assertJsonKeyNotIn(response,('foo','xxx'))

    def Test_assertJsonKeyNotIn_False(self):
        response=MockResponse(body=json.dumps({'bar':'foo'}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonKeyNotIn(response,('bar',))

    '''
    Test of assertJsonFieldEqual
    
    def Test_assertJsonFieldEqual_True_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        self.tc.assertJsonFieldEqual(response,json_path='foo',exp_value='bar')

    def Test_assertJsonFieldEqual_False_depth_one(self):
        response=MockResponse(body=json.dumps({'foo':'bar'}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonFieldEqual(response,json_path='foo',exp_value='xxx')

    def Test_assertJsonFieldEqual_True_depth_two(self):
        response=MockResponse(body=json.dumps({'foo':{'bar':'value'}}))
        self.tc.assertJsonFieldEqual(response,json_path='foo.bar',exp_value='value')

    def Test_assertJsonFieldEqual_False_depth_two(self):
        response=MockResponse(body=json.dumps({'foo':{'bar':'value'}}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonFieldEqual(response,json_path='foo.bar',exp_value='xxx')

    def Test_assertJsonFieldEqual_True_bool(self):
        response=MockResponse(body=json.dumps({'foo':True}))
        self.tc.assertJsonFieldEqual(response,json_path='foo',exp_value=True)

    def Test_assertJsonFieldEqual_False_bool(self):
        response=MockResponse(body=json.dumps({'foo':True}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonFieldEqual(response,json_path='foo',exp_value=False)

    def Test_assertJsonFieldEqual_True_int(self):
        response=MockResponse(body=json.dumps({'foo':0}))
        self.tc.assertJsonFieldEqual(response,json_path='foo',exp_value=0)

    def Test_assertJsonFieldEqual_False_int(self):
        response=MockResponse(body=json.dumps({'foo':0}))
        with self.tc.assertRaises(AssertionError):
            self.tc.assertJsonFieldEqual(response,json_path='foo',exp_value=1)

    def Test_assertJsonFieldEqual_True_path_with_period(self):
        response=MockResponse(body=json.dumps({'foo.bar':'xxx'}))
        self.tc.assertJsonFieldEqual(response,json_path='foo.bar',exp_value='xxx')            
    '''
class MockResponse(object):

    def __init__(self,status=None, headers=None, body=None):
        self.status=status
        self.headers=headers
        self.body=body

if __name__=='__main__':
    unittest.main()