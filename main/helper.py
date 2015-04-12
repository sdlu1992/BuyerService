__author__ = 'sdlu'
import json, hashlib, time
from main.models import Buyer, Category
from django.shortcuts import render, HttpResponse, render_to_response, HttpResponseRedirect


def get_login_info(request):
    try:
        req = json.loads(request.body)
        r_phone = req['phone']
        r_password = req['password']
        r_platform = req['platform']
    except Exception:
        r_phone = request.POST.get('phone')
        r_password = request.POST.get('password')
        r_platform = request.POST.get('platform')

    return r_phone, r_password, r_platform


def get_register_info(request):
    r_phone, r_password, r_platform = get_login_info(request)
    try:
        req = json.loads(request.body)
        r_email = req['email']
        r_name = req['name']
    except Exception:
        r_email = request.POST.get('email')
        r_name = request.POST.get('name')

    return r_phone, r_password, r_platform, r_email, r_name
