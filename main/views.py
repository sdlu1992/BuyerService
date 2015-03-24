#coding=utf-8
from django.shortcuts import HttpResponse
import json, hashlib, time
from main.models import Buyer, Category
# Create your views here.


def register(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        req = json.loads(request.body)
        r_name = req['name']
        r_password = req['password']
        print r_name, r_password
        r_phone = req['phone']
        r_email = req['email']
        print r_name, r_password, r_phone, r_email
        if r_name == '':
            error_message = 'name is empty'
        elif r_password == '':
            error_message = 'password is empty'
        elif r_phone == '':
            error_message = 'phone is empty'
        else:
            buyer = get_buyer_by_phone(r_phone)
            if len(buyer) == 0:
                buyer = Buyer(name=r_name, phone=r_phone, nickname=r_name, type=1, email=r_email, password=r_password,
                              credit=0)
                buyer.save()
                response['response'] = 1
            else:
                error_message = 'phone has registered'
    response['error_msg'] = error_message
    json.dumps(response)
    j = json.dumps(response)
    print j
    return HttpResponse(j)


def login(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        req = json.loads(request.body)
        r_phone = req['phone']
        r_password = req['password']
        print r_phone, r_password,
        if r_phone == '':
            error_message = 'name is empty'
        elif r_password == '':
            error_message = 'token is empty, please relogin'
        else:
            buyer = get_buyer_by_phone(r_phone)
            if len(buyer) == 1:
                if r_password == buyer[0].password:
                    token = get_token(r_password)
                    buyer[0].token = token
                    buyer[0].save()
                    info = {'name': buyer[0].name, 'phone': buyer[0].phone, 'email': buyer[0].email}
                    response['response'] = 1
                    response['token'] = token
                    response['info'] = info
                else:
                    error_message = 'password is wrong'
            else:
                error_message = 'phone has not registered'
    response['error_msg'] = error_message
    json.dumps(response)
    j = json.dumps(response)
    print j
    return HttpResponse(j)


def info(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        req = json.loads(request.body)
        buyer = Buyer.objects.filter(token=req['token'])
        if len(buyer) == 1:
            info = {'name': buyer[0].name, 'phone': buyer[0].phone, 'email': buyer[0].email}
            response['response'] = 1
            response['info'] = info
    json.dumps(response)
    j = json.dumps(response)
    return HttpResponse(j)


def category(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    c1 = {'10': '手机', '11': '手机配件', '12':'数码相机'}
    c2 = {'20': '板鞋', '21': '跑鞋', '22': '皮鞋'}
    c0 = {'1': c1, '2': c2}
    c_root = {'1': '手机数码', '2': '鞋类'}
    cc = Category(category=c0, root_category=c_root)
    cc.save()
    if request.method == 'GET':
        ca = Category.objects.all()
        # response['category'] = ca.last().category
        response['category'] = c0
        # response['root'] = str(ca.last().root_category).replace('\\', '%')
        response['root'] = c_root
    j = json.dumps(response)
    # j = json.JSONEncoder().encode(response)
    return HttpResponse(j)


def get_buyer_by_phone(phone_number):
    buyer = Buyer.objects.filter(phone=phone_number)
    print buyer
    return buyer


def get_token(r_password):
    m = hashlib.md5()
    print r_password
    print time.time()
    m.update(r_password+str(time.time()))
    return m.hexdigest()
