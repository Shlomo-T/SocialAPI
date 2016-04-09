from social.backends.google import *
import json,ssl
from social.strategies.django_strategy import DjangoStrategy
from API.models import User
from datetime import datetime



class Helper:
    ''' class th handle logic that needed for registering user to the system '''

    def validate_request_body(request):
        ''' function for validating the request
            the request should use POST method and the body should contain JSON with two fields
            {
                'backend':'xxx',
                'access_token:'xxx'
            }
                this version support only Google authenticatin
        '''
        ans=False
        ac=None
        if request.method == 'POST' and request.data is not None:
            data = request.data

            if data['backend'] is not None and data['backend'] == 'google' and data['access_token'] is not None and data['access_token'] != '':
                ac = data['access_token']
                ans=True
        return ans,ac

    def register_by_access_token(access_token):
        ''' registering user to the system if access toke is valid '''
        ex= None
        user=None
        alreadyExist=False
        try:
            strategy = DjangoStrategy(None)
            backend = GoogleOAuth2(strategy)
            s = backend.get_scope()
            userdata = backend.user_data(access_token)
            if userdata is not None and userdata['email'] is not None and userdata['email']!='':
                user= Helper.build_user(userdata,access_token)
                if user is not None:
                    alreadyExist= Helper.user_already_exist(user)
                    if not alreadyExist:
                        user.save();
                    else:
                        Helper.update_token(user,access_token)

        except Exception as e:
            ''' todo: write exception to logger'''
            user=None;
            ex=e

        return user,ex,alreadyExist

    def build_user(userdata,access_token):
        '''building User model'''
        user=None
        firstName=''
        lastName=''
        try:
            email=userdata['email']
            if userdata['given_name'] is not None:
                firstName= userdata['given_name']

            if userdata['family_name'] is not None:
                lastName = userdata['family_name']

            if userdata['email'] is not None:
                user= User(first_name=firstName,last_name=lastName,email=email,access_token=access_token,token_last_update=datetime.utcnow())
        except Exception as e:
            ''' todo: write exception to logger'''
            user= None
        return user

    def user_already_exist(user):
        ''' check if the user already exist in the DB'''

        ans=True
        try:
            if not User.objects.filter(email=user.email):
                ans=False
        except Exception as e:
            ''' todo: write exception to logger '''
            ans= True
        return ans

    def update_token(user,access_token):
        ''' update access_token for existing user if the token has changed since last update '''
        curr_user= User.objects.filter(email=user.email).first()
        if curr_user.access_token != user.access_token:
            curr_user.access_token=user.access_token
            curr_user.token_last_update=datetime.utcnow()
            curr_user.save()

    def build_response(user,e,alreadyExist):
        '''build reponse by registration output '''

        if user is not None:
            return {'id': user.email , 'token':user.access_token, 'is_new': not alreadyExist}

        elif e is not None:
            return { 'Error':str(e)}