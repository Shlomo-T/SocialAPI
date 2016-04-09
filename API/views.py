from django.shortcuts import render
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from social.backends.google import GoogleOAuth2
from social.strategies.django_strategy import DjangoStrategy
import urllib

# Create your views here.
@api_view(['GET', 'POST'])
def Auth(request):
    if request.method == 'POST':
        data=request.data

        if data['backend']=='google' and data['access_token']!='':
            ac=data['access_token']
            #user = Helper.register_by_access_token(ac,GoogleOAuth2())
            #user=Helper.register_by_access_token_http(ac)
            strategy= DjangoStrategy(None)
            backend=GoogleOAuth2(strategy)
            s=backend.get_scope()
            uuser= backend.user_data(ac)

        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})


