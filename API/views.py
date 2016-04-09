from django.shortcuts import render
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from social.backends.google import GoogleOAuth2
from API.AuthHelper import Helper
import urllib

# Create your views here.
@api_view( ['POST'])
def Auth(request):
    validate,access_token= Helper.validate_request_body(request)
    if validate:
        user,e, alreadyExist= Helper.register_by_access_token(access_token)

        response=Helper.build_response(user,e,alreadyExist)
        return Response(response)
    return Response({"Error": "request is not valid"})


