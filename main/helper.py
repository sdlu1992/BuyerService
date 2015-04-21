__author__ = 'sdlu'
import json, hashlib, time
from main.models import Buyer, Category, Goods
from django.forms.models import model_to_dict
from django.shortcuts import render, HttpResponse, render_to_response, HttpResponseRedirect


def get_login_info(request):
    try:
        req = json.loads(request.body)
        print req
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


def get_good_dic_by_model(good):
    dic_good = model_to_dict(good)
    try:
        dic_good['image_url_title'] = good.image_url_title.url
    except ValueError:
        dic_good['image_url_title'] = ''
    try:
        dic_good['image1'] = good.image1.url
    except ValueError:
        dic_good['image1'] = ''
    try:
        dic_good['image2'] = good.image2.url
    except ValueError:
        dic_good['image2'] = ''
    try:
        dic_good['image3'] = good.image3.url
    except ValueError:
        dic_good['image3'] = ''
    try:
        dic_good['image4'] = good.image4.url
    except ValueError:
        dic_good['image4'] = ''
    return dic_good
