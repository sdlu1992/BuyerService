#coding=utf-8
import json, hashlib, time
from main.models import Buyer, Category, Store, Goods
from django.shortcuts import render, HttpResponse, render_to_response, HttpResponseRedirect
from helper import get_login_info, get_register_info
# Create your views here.


def register(request):
    response = {'response': '2'}
    error_message = ''
    r_platform = 'android'
    print(request.method)
    if request.method == 'POST':
        r_phone, r_password, r_platform, r_email, r_name = get_register_info(request)
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
    elif request.method == 'GET':
        return render_to_response('register.html', locals())

    response['error_msg'] = error_message
    json.dumps(response)
    j = json.dumps(response)
    if r_platform == 'web':
        if response['response'] == 1:
            return HttpResponseRedirect('/login')
        else:
            return render_to_response('register.html', locals())
    elif r_platform == 'android':
        return HttpResponse(j)


def login(request):
    r_platform = 'android'
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'GET':
        return render_to_response('login.html', locals())
    if request.method == 'POST':
        r_phone, r_password, r_platform = get_login_info(request)
        print r_phone, r_password, r_platform
        if r_phone == '':
            error_message = 'name is empty'
        elif r_password == '':
            error_message = 'token is empty, please relogin'
        else:
            buyer = get_buyer_by_phone(r_phone)
            print len(buyer)
            if len(buyer) == 1:
                if r_password == buyer[0].password:
                    token = get_token(r_password)
                    buyer[0].token = token
                    buyer[0].save()
                    info = {'name': buyer[0].name, 'phone': buyer[0].phone, 'email': buyer[0].email}
                    response['response'] = 1
                    response['token'] = token
                    response['info'] = info
                    request.session['token'] = token
                else:
                    error_message = 'password is wrong'
            else:
                error_message = 'phone has not registered'
    response['error_msg'] = error_message
    json.dumps(response)
    j = json.dumps(response)
    print j
    if r_platform == 'web':
        if response['response'] == 1:
            return HttpResponseRedirect('/info')
        else:
            return render_to_response('login.html', locals())
    elif r_platform == 'android':
        return HttpResponse(j)


def info(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    print(request.method)

    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        info = {'name': buyer[0].name, 'phone': buyer[0].phone, 'email': buyer[0].email}
        user = buyer[0]
        response['response'] = 1
        response['info'] = info
    else:
        return HttpResponseRedirect('/login')
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def change_to_solder(request):
    print(request.method)
    user = None
    error_message = ''
    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token=request.session.get('token', ''))
    if len(buyer) == 1:
        buyer[0].type = 2
        buyer[0].save()
        user = buyer[0]
        store = Store(name=str(user.name)+"的商店", owner=user, address='', credit=0)
        store.save()
        error_message = "成功！"
    else:
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/info', locals())


def new_goods(request):
    user = None
    error_message = ''
    token = request.session.get('token', '')
    r_platform = 'web'
    buyer = Buyer.objects.filter(token=request.session.get('token', ''))
    cc, cMerge = get_category()
    if token == '':
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        return render_to_response('new_goods.html', locals())
    elif request.method == 'POST':
        g_name = request.POST.get('goods_name', '')
        g_price = request.POST.get('price', 0)
        g_category = request.POST.get('category', '')
        print g_name, g_price, g_category

    if len(buyer) == 1:
        buyer[0].type = 2
        buyer[0].save()
        user = buyer[0]
        store = Store.objects.filter(owner=user)
        if len(store) == 1:
            goods = Goods(name=g_name, price=g_price, category=g_category, store=store[0])
            goods.save()
            error_message = '成功！'
    else:
        return HttpResponseRedirect('/login')
    # root = json.dumps(c_root)
    # cate = json.dumps(cate)
    return render_to_response('new_goods.html', locals())


def category(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    cc, cMerge = get_category()
    cc.save()
    if request.method == 'GET':
        ca = Category.objects.all()
        # response['category'] = ca.last().category
        response['category'] = cc.category
        # response['root'] = str(ca.last().root_category).replace('\\', '%')
        response['root'] = cc.root_category
    j = json.dumps(response)
    # j = json.JSONEncoder().encode(response)
    return HttpResponse(j)


def get_goods_by_category(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        cate = req['category']
        goods = Goods.objects.filter(category=cate)
        response['len'] = len(goods)
        if len(goods) != 0:
            response['goods'] = goods
        response['response'] = '1'

    print response
    response['error_msg'] = error_message
    print response
    j = json.dumps(response)
    print response
    return HttpResponse(j)


def report(request):

    return render_to_response('goods_list.html', locals())


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


def get_category():
    c1 = {'10': '手机', '11': '手机配件', '12':'数码相机'}
    c2 = {'20': '板鞋', '21': '跑鞋', '22': '皮鞋'}
    c0 = {'1': c1, '2': c2}
    c_root = {'1': '手机数码', '2': '鞋类'}
    print c0
    cMerge = dict(c1, **c2)
    cc = Category(category=c0, root_category=c_root)
    return cc, cMerge