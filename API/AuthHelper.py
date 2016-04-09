from social.backends.google import *
import json,ssl
from urllib.request import urlopen,build_opener,install_opener,HTTPSHandler
class Helper:
    def register_by_access_token(access_token, backend):
        user=backend.user_data(access_token)
        return user

    def register_by_access_token_http(access_token):
        baseUrl='https://www.googleapis.com/plus/v1/people/me?access_token='
        https_sslv3_handler = HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv3))
        opener = build_opener(https_sslv3_handler)
        install_opener(opener)
        userinfo = urlopen(baseUrl+access_token)
        info=userinfo.read();
        if info is not None and info != '':
            data=json.load(info)