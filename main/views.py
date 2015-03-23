from django.shortcuts import HttpResponse
import json, hashlib, time
from main.models import Buyer
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
            buyers = get_buyer_by_phone(r_phone)
            if len(buyers) == 1:
                if r_password == buyers[0].password:
                    token = get_token(r_password)
                    buyers[0].token = token
                    buyers[0].save()
                    info = {'name': buyers[0].name, 'phone': buyers[0].phone, 'email': buyers[0].email}
                    response['response'] = 1
                    response['token'] = token
                    response['info'] = info
                else:
                    error_message = 'password is wrong'
            else:
                error_message = 'phone has not registered'
    response['error_msg'] = error_message
    j = json.dumps(response)
    print j
    return HttpResponse(j)


def get_info(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        buyer = get_buyer_by_token(request)
        if buyer != 3:
            info = {'name': buyer.name, 'phone': buyer.phone, 'email': buyer.email}
            response['response'] = 1
            response['info'] = info
        else:
            error_message = '没有这个用户'
    response['error_msg'] = error_message
    j = json.dumps(response)
    return HttpResponse(j)


def get_buyer_by_phone(phone_number):
    buyer = Buyer.objects.filter(phone=phone_number)
    print buyer
    return buyer


def get_buyer_by_token(request):
    req = json.loads(request.body)
    token = req['token']
    buyers = Buyer.objects.filter(token=token)
    if len(buyers) == 1:
        return buyers[0]
    else:
        return 3


def get_token(r_password):
    m = hashlib.md5()
    print r_password
    print time.time()
    m.update(r_password+str(time.time()))
    return m.hexdigest()
