#encoding=utf-8
from functools import wraps
from util.redis_client import RedisClient
from conf.settings import AUTHEN_TOKEN_KEY

def auth(method):
    def auth1(response):
        def _check_auth_token(self,request_data):
            token = request_data.get("token","")
            if token:
                ret = RedisClient().client.get(AUTHEN_TOKEN_KEY % token)
                if ret:
                    return response(self,request_data)
                else:
                    return {"data":{},"status":-1,"err_msg":"页面已失效"}
            else:
                session = self.get_cookie("session_id")
                print session," post"
                if session:
                    ret = RedisClient().client.get(AUTHEN_TOKEN_KEY % session)
                    if ret:
                        return response(self,request_data)
                return {"data":{},"status":-1,"err_msg":"页面已失效"}
        return _check_auth_token

    def auth2(response):
        def _check_post_session(self,request_data):
            session = self.get_cookie("session_id")
            print session," post"
            if session:
                ret = RedisClient().client.get(AUTHEN_TOKEN_KEY % session)
                if ret:
                    return response(self,request_data)
            return {"data":{},"status":-1,"err_msg":"页面已失效"}
        return _check_post_session

    def auth3(response):
        def _check_get_session(self):
            session = self.get_cookie("session_id")
            print session," get"
            if session:
                ret = RedisClient().client.get(AUTHEN_TOKEN_KEY % session)
                print ret,AUTHEN_TOKEN_KEY % session
                if ret:
                    print "in auth3"
                    return response(self)
            return {"data":{},"status":-1,"err_msg":"页面已失效"}
        return _check_get_session

    if method == "token":
        return auth1
    if method == "post":
        return auth2
    if method == "get":
        return auth3
    if not method:
       raise Exception,"lost param"
