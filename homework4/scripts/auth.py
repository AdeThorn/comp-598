import tornado
from tornado.web import RequestHandler


def get_user(request_handler):
    request = request_handler.request
    args = request.query_arguments
    if "username" in args and "password" in args:
        if args["username"][0].decode("utf-8")=="nyc" and args["password"][0].decode("utf-8")=="iheartnyc":
            print(args)
            return 1#request_handler.get_cookie("user")
        
    return None


login_url = "/login"
#def get_login_url(request_handler):
#    pass
