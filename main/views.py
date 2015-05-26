# coding=utf-8
import json
import hashlib
import time
import datetime
import string
import random

from django.forms.models import model_to_dict
from django.db.models import Count
from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect

from main.models import Buyer, Category, Store, Goods, BuyHistory, WishList, Order, Appraise, Collect, Address
from helper import get_login_info, get_register_info, get_good_dic_by_model
from form_new_goods import NewGoodForm

# Create your views here.

import sys

print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()


def register(request):
    response = {'response': '2'}
    error_message = ''
    r_platform = 'android'
    print(request.method)
    if request.method == 'POST':
        r_phone, r_password, r_platform, r_email, r_name = get_register_info(request)
        if r_name == '':
            error_message = 'name is empty'
        elif r_password == '':
            error_message = 'password is empty'
        elif r_phone == '':
            error_message = 'phone is empty'
        else:
            buyer = get_buyer_by_phone(r_phone)
            if len(buyer) == 0:
                buyer = Buyer(name=r_name, phone=r_phone, type=1, email=r_email, password=r_password,
                              credit=0, money=0)
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
            error_message = 'password is empty'
        else:
            buyer = get_buyer_by_phone(r_phone)
            print len(buyer)
            if len(buyer) == 1:
                if r_password == buyer[0].password:
                    user = buyer[0]
                    token = get_token(r_password)
                    if r_platform == 'android':
                        buyer[0].token = token
                    elif r_platform == 'web':
                        buyer[0].token_web = token
                    buyer[0].save()
                    info = model_to_dict(user)
                    info['token_web'] = ''
                    info['password'] = ''
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
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        info = model_to_dict(user)
        info['token_web'] = ''
        info['password'] = ''
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
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    if len(buyer) == 1:
        buyer[0].type = 2
        buyer[0].save()
        user = buyer[0]
        store = Store(name=str(user.name + "\'s Store").encode('utf-8'), owner=user, address='', credit=0)
        store.save()
        error_message = "成功！"
    else:
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/info', locals())


def new_goods(request):
    user = None
    error_message = ''
    token = request.session.get('token', '')
    print token
    r_platform = 'web'
    buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    cc, cMerge = get_category()
    g_image = ''
    if token == '':
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        if len(buyer) == 1:
            user = buyer[0]
        return render_to_response('new_goods.html', locals())
    elif request.method == 'POST':
        form = NewGoodForm(request.POST, request.FILES)
        g_name = request.POST.get('goods_name', '')
        g_content = request.POST.get('goods_content', '')
        g_price = request.POST.get('price', 0)
        g_category = request.POST.get('category', '')
        if form.is_valid():
            g_image = form.cleaned_data['image_title']
            g_image1 = form.cleaned_data['image1']
            g_image2 = form.cleaned_data['image2']
            g_image3 = form.cleaned_data['image3']
            g_image4 = form.cleaned_data['image4']
        else:
            error_message = 'form wrong'

    if len(buyer) == 1 and error_message == '':
        buyer[0].type = 2
        buyer[0].save()
        user = buyer[0]
        store = Store.objects.filter(owner=user)
        if len(store) == 1:
            goods = Goods(name=g_name, price=g_price, category=g_category, store=store[0], image_url_title=g_image,
                          image1=g_image1, image2=g_image2, image3=g_image3, image4=g_image4, des=g_content)
            goods.save()
            error_message = '成功！'
    else:
        return HttpResponseRedirect('/login')
    return render_to_response('new_goods.html', locals())


def category(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    cc, cMerge = get_category()
    if request.method == 'GET':
        response['category'] = cc.category
        response['root'] = cc.root_category
    j = json.dumps(response)
    return HttpResponse(j)


def get_goods_by_category(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        cate = req['category']
        # cate = request.POST.get('test')
        goods = Goods.objects.filter(category=cate)
        response['len'] = len(goods)
        if len(goods) != 0:
            goods.reverse()
            r_goods = []
            for foo in goods:
                # dic = {'id': foo.id, 'title': foo.name, 'price': foo.price, 'des': foo.des, 'category': foo.category,
                # 'store': foo.store.id, 'count': len(BuyHistory.objects.filter(goods=foo)),
                # 'store_name': foo.store.name}
                dic = get_good_dic_by_model(foo)
                print dic
                dic['count'] = len(BuyHistory.objects.filter(goods=foo).exclude(state=0))
                dic['store'] = model_to_dict(foo.store)
                print dic['store']
                r_goods.insert(0, dic)
            response['goods'] = r_goods
        response['response'] = '1'

    response['error_msg'] = error_message
    j = json.dumps(response)
    return HttpResponse(j)


def get_goods_by_search(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    dict_relevancy = {}
    if request.method == 'POST':
        # r_platform = request.POST.get('platform')
        # search_key = request.POST.get('test')
        # buyer = Buyer.objects.filter(token_web=request.session.get('token'))
        req = json.loads(request.body)
        print req
        search_key = req['search_key']
        search_keys = search_key.split(' ')
        goods = Goods.objects.filter(name__icontains=search_key)
        for key in search_keys:
            t_goods = Goods.objects.filter(name__icontains=key)
            for good in t_goods:
                if goods.filter(id=good.id).exists():
                    try:
                        dict_relevancy[good.id] += 1
                    except KeyError:
                        dict_relevancy[good.id] = 1
                else:
                    goods |= t_goods.filter(id=good.id)

        response['len'] = len(goods)
        if len(goods) != 0:
            r_goods = []
            for foo in goods:
                dic = get_good_dic_by_model(foo)
                dic['count'] = len(BuyHistory.objects.filter(goods=foo).exclude(state=0))
                dic['store'] = model_to_dict(foo.store)
                try:
                    dic['relevancy'] = dict_relevancy[foo.id]
                except KeyError:
                    dic['relevancy'] = 0
                r_goods.append(dic)
            # 根据相关度排序
            r_goods.sort(lambda x, y: cmp(x['relevancy'], y['relevancy']))
            r_goods.reverse()
            response['goods'] = r_goods
        response['response'] = '1'

    response['error_msg'] = error_message
    j = json.dumps(response)
    return HttpResponse(j)


def report(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    goods = []
    print(request.method)

    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        goods_list = Goods.objects.filter(store=user.store)
        for good in goods_list:
            dic = get_good_dic_by_model(good)
            dic['count'] = len(BuyHistory.objects.filter(goods=good).exclude(state=0))
            goods.append(dic)
        response['response'] = 1
        response['info'] = info
    else:
        return HttpResponseRedirect('/login')
    if r_platform == 'web':
        return render_to_response('goods_list.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_good(request):
    response = {'response': '2'}
    error_message = ''
    print(request.method)
    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        good_id = req['good_id']
        # good_id = request.POST.get('test')
        goods = Goods.objects.filter(id=good_id)
        buyer = Buyer.objects.filter(token=req['token'])
        if len(goods) != 0:
            good = goods[0]
            dic_good = get_good_dic_by_model(good)
            print dic_good
            dic_good['count'] = len(BuyHistory.objects.filter(goods=good).exclude(state=0))
            try:
                collect = Collect.objects.get(goods=good, buyer=buyer[0])
                dic_good['isCollect'] = collect.is_collect
            except Exception:
                dic_good['isCollect'] = 0
            store = good.store
            solder = store.owner
            response['good'] = dic_good
            response['response'] = '1'
            response['store'] = model_to_dict(store)
            response['solder'] = model_to_dict(solder)
            response['solder']['token'] = ''
            response['solder']['password'] = ''

    response['error_msg'] = error_message
    j = json.dumps(response)
    print j
    return HttpResponse(j)


def add_wish_list(request):
    count = ''
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    goods = None
    print(request.method)

    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        print req
        r_platform = req['platform']
        good_id = req['good_id']
        count = req['count']
        buyer = Buyer.objects.filter(token=req['token'])
        goods = Goods.objects.filter(id=good_id)
    if len(buyer) == 1 and len(goods) == 1:
        user = buyer[0]
        good = goods[0]
        wish_exist = WishList.objects.filter(goods=good, buyer=user, dele=1)
        if len(wish_exist) == 1:
            wish = wish_exist[0]
            wish.amount += int(count)
            wish.date = datetime.datetime.now()
        else:
            wish = WishList(amount=count, goods=good, buyer=user, date=datetime.datetime.now(), dele=1)
        wish.save()
        response['response'] = 1
    else:
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_wish_list(request):
    count = ''
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        wish_list = WishList.objects.filter(buyer=user, dele=1)
        response['len'] = len(wish_list)
        if len(wish_list) != 0:
            wish_list.reverse()
            wishes = []
            for foo in wish_list:
                dic = model_to_dict(foo)
                dic['good'] = get_good_dic_by_model(foo.goods)
                dic['store'] = model_to_dict(foo.goods.store)
                wishes.insert(0, dic)
            response['wish_list'] = wishes
        else:
            pass
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def add_order(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    r_goods = ''
    goods = []
    price_total = 0
    counts = []
    wishes_json = None
    print(request.method)

    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        # req = json.loads(request.POST.get('test'))
        print req
        r_platform = req['platform']
        r_goods = json.loads(req['goods'])
        r_address_id = req['address_id']
        address1 = Address.objects.get(id=r_address_id)
        buyer = Buyer.objects.filter(token=req['token'])
        try:
            wishes_json = json.loads(req['wish_list'])
            for foo in wishes_json:
                wish = WishList.objects.get(id=foo['id'])
                wish.dele = 0
                wish.save()
        except Exception:
            print wishes_json is None
        for foo in r_goods:
            good = Goods.objects.get(id=foo['id'])
            goods.append(good)
            price_total += good.price * string.atoi(foo['count'])
            counts.append(foo['count'])
    print len(buyer)
    if len(buyer) == 1 and len(goods) != 0:
        user = buyer[0]
        order = Order(goods=r_goods, buyer=user, date=datetime.datetime.now(), state=0,
                      price=price_total, address=address1)
        order.save()
        for index, foo in enumerate(goods):
            history = BuyHistory(buyer=user, goods=foo, price=foo.price, amount=counts[index],
                                 order=order, state=0, date=order.date)
            history.save()
        response['response'] = 1
        response['order_id'] = order.id
    elif len(goods) == 0:
        error_message = 'No this goods'
    response['error_msg'] = error_message
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_order(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    order = None
    order_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        r_platform = req['platform']
        buyer = Buyer.objects.filter(token=req['token'])
        order_id = req['order_id']
        # r_platform = request.POST.get('platform')
        # order_id = request.POST.get('test')
        # buyer = Buyer.objects.filter(token_web=request.session.get('token'))
    if len(buyer) == 1:
        user = buyer[0]
        order = Order.objects.get(id=order_id)
        histories = BuyHistory.objects.filter(order=order)
        if len(histories) != 0:
            his_dic = []
            for foo in histories:
                dic = model_to_dict(foo)
                dic['good'] = get_good_dic_by_model(foo.goods)
                dic['store'] = model_to_dict(foo.goods.store)
                dic['solder'] = model_to_dict(foo.goods.store.owner)
                dic['solder']['password'] = ''
                apps = Appraise.objects.filter(buy_history=foo)
                if len(apps) != 0:
                    dic['appraise'] = model_to_dict(apps[0])
                else:
                    dic['appraise'] = ''
                his_dic.append(dic)
            response['history_list'] = his_dic
            j_buyer = model_to_dict(user)
            j_buyer['password'] = ''
            response['buyer'] = j_buyer
            response['len'] = len(histories)
            response['order'] = model_to_dict(order)
            response['order']['address'] = model_to_dict(order.address)
        else:
            pass
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_buy_history(request):
    count = ''
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        histories = BuyHistory.objects.filter(buyer=user)
        response['len'] = len(histories)
        if len(histories) != 0:
            his_dic = []
            for foo in histories:
                dic = model_to_dict(foo)
                dic['good'] = get_good_dic_by_model(foo.goods)
                dic['store'] = model_to_dict(foo.goods.store)
                his_dic.insert(0, dic)
            response['history_list'] = his_dic
        else:
            pass
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        j = json.dumps(response)
        return HttpResponse(j)


def pay_for_goods(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    order_id = ''
    history_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        order_id = req['order_id']
        history_id = req['history_id']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        order = Order.objects.get(id=order_id)
        if history_id == '':
            histories = BuyHistory.objects.filter(order=order, state=0)
        else:
            histories = BuyHistory.objects.filter(order=order, state=0, id=history_id)
        if len(histories) != 0:
            total = 0
            for foo in histories:
                total += foo.price * foo.amount
            if user.money < total:
                response['response'] = 5
                error_message = 'money not enough'
                histories = []
            else:
                user.money -= total
                user.save()
            for foo in histories:
                foo.state = 1
                foo.save()
                response['history'] = model_to_dict(foo)
                response['response'] = 1
        else:
            response['response'] = 3
            error_message = 'no this history'
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    if r_platform == 'web':
        return HttpResponseRedirect('/info')
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def take_goods(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    order_id = ''
    history_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        order_id = req['order_id']
        history_id = req['history_id']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        order = Order.objects.get(id=order_id)
        if history_id == '':
            histories = BuyHistory.objects.filter(order=order, state=2)
        else:
            histories = BuyHistory.objects.filter(order=order, state=2, id=history_id)
        if len(histories) != 0:
            for foo in histories:
                foo.state = 3
                foo.goods.store.owner.money += foo.price * foo.amount
                foo.save()
                response['history'] = model_to_dict(foo)
                response['response'] = 1
        else:
            response['response'] = 3
            error_message = 'no this history'
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    if r_platform == 'web':
        return HttpResponseRedirect('/info')
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def deliver_goods(request):
    response = {'response': '2'}
    error_message = ''
    buyer = None
    history_id = ''
    print(request.method)

    if request.method == 'POST':
        history_id = request.POST.get('history_id')
        buyer = Buyer.objects.filter(token_web=request.session.get('token'))
    if len(buyer) == 1:
        histories = BuyHistory.objects.filter(state=1, id=history_id)
        if len(histories) != 0:
            for foo in histories:
                foo.state = 2
                foo.save()
                response['history'] = model_to_dict(foo)
                response['response'] = 1
        else:
            response['response'] = 3
            error_message = 'no this history'
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    return HttpResponseRedirect('/getOrderListWeb')


def apply_refund(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    order_id = ''
    history_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        order_id = req['order_id']
        history_id = req['history_id']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        order = Order.objects.get(id=order_id)
        if history_id == '':
            histories = BuyHistory.objects.filter(order=order)
        else:
            histories = BuyHistory.objects.filter(order=order, id=history_id)
        if len(histories) != 0:
            for foo in histories:
                foo.state = 5
                foo.save()
                response['history'] = model_to_dict(foo)
                response['response'] = 1
        else:
            response['response'] = 3
            error_message = 'no this history'
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    if r_platform == 'web':
        return HttpResponseRedirect('/info')
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def refund_decide(request):
    response = {'response': '2'}
    error_message = ''
    buyer = None
    history_id = ''
    print(request.method)

    if request.method == 'POST':
        history_id = request.POST.get('history_id')
        buyer = Buyer.objects.filter(token_web=request.session.get('token'))
    if len(buyer) == 1:
        histories = BuyHistory.objects.filter(state=5, id=history_id)
        if len(histories) != 0:
            for foo in histories:
                foo.state = 6
                foo.goods.store.owner.money -= foo.price * foo.amount
                foo.buyer.money += foo.price * foo.amount
                foo.save()
                response['history'] = model_to_dict(foo)
                response['response'] = 1
        else:
            response['response'] = 3
            error_message = 'no this history'
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    return HttpResponseRedirect('/getOrderListWeb')


def appraise(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    history_id = ''
    order_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        r_platform = req['platform']
        history_id = req['history_id']
        order_id = req['order_id']
        content = req['content']
        appraise_type = req['type']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]

        if order_id == '' or order_id is None:
            histories = BuyHistory.objects.filter(id=history_id)
        elif history_id == '' or history_id is None:
            order = Order.objects.get(id=order_id)
            histories = BuyHistory.objects.filter(order=order)
        else:
            order = Order.objects.get(id=order_id)
            histories = BuyHistory.objects.filter(id=history_id, order=order)
        if len(histories) != 0:
            for foo in histories:
                app = Appraise(type=int(appraise_type), buy_history=foo, content=content,
                               date=datetime.datetime.now(), goods=foo.goods)
                app.save()
                foo.state = 4
                foo.save()
                foo.goods.store.credit += (1 - app.type)
                foo.goods.store.save()
            response['response'] = 1
        else:
            response['response'] = 3
            error_message = 'no this history'
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    if r_platform == 'web':
        return HttpResponseRedirect('/info')
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_appraise_list(request):
    count = ''
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    good_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        good_id = req['good_id']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        goods = Goods.objects.filter(id=good_id)
        if len(goods) != 0:
            good = goods[0]
            histories = BuyHistory.objects.filter(goods=good)
            appraises = Appraise.objects.filter(goods=good)
            app_dic = []
            response['len'] = len(appraises)
            for foo in appraises:
                dic = model_to_dict(foo)
                dic['username'] = foo.buy_history.buyer.name
                app_dic.insert(0, dic)
            response['appraise_list'] = app_dic
            response['total_good'] = len(appraises.filter(type=0))
            response['total_middle'] = len(appraises.filter(type=1))
            response['total_bad'] = len(appraises.filter(type=2))
        else:
            response['response'] = 3
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        j = json.dumps(response)
        return HttpResponse(j)


def recharge(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    rechar = 0
    print(request.method)

    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        print req
        rechar = req['money']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        user.money += int(rechar)
        user.save()
        response['response'] = 1
    else:
        return HttpResponseRedirect('/login')
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def add_collection(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    goods = None
    print(request.method)

    if request.method == 'GET':
        token = request.session.get('token', '')
        r_platform = 'web'
        if token == '':
            return HttpResponseRedirect('/login')
        else:
            buyer = Buyer.objects.filter(token_web=request.session.get('token', ''))
    elif request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        good_id = req['good_id']
        buyer = Buyer.objects.filter(token=req['token'])
        goods = Goods.objects.filter(id=good_id)
    if len(buyer) == 1 and len(goods) == 1:
        user = buyer[0]
        good = goods[0]
        collect_exist = Collect.objects.filter(goods=good, buyer=user)
        if len(collect_exist) == 1:
            collect = collect_exist[0]
            if collect.is_collect == 1:
                collect.is_collect = 0
            else:
                collect.is_collect = 1
        else:
            collect = Collect(goods=good, buyer=user, is_collect=1)
        collect.save()
        response['response'] = 1
        response['collect'] = model_to_dict(collect)
        response['collect']['good'] = get_good_dic_by_model(collect.goods)
        response['collect']['store'] = model_to_dict(collect.goods.store)
    else:
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_collection_list(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        buyer = Buyer.objects.filter(token=req['token'])

    if len(buyer) == 1:
        user = buyer[0]
        collections = Collect.objects.filter(buyer=user)
        response['len'] = len(collections)
        if len(collections) != 0:
            colle_dic = []
            for foo in collections:
                dic = model_to_dict(foo)
                dic['good'] = get_good_dic_by_model(foo.goods)
                dic['good']['count'] = len(BuyHistory.objects.filter(goods=foo.goods).exclude(state=0))
                dic['store'] = model_to_dict(foo.goods.store)
                colle_dic.insert(0, dic)
            response['collect_list'] = colle_dic
        else:
            pass
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        j = json.dumps(response)
        return HttpResponse(j)


def get_home(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        buyer = Buyer.objects.filter(token=req['token'])
        # r_platform = request.POST.get('platform')
        # order_id = request.POST.get('test')
        # buyer = Buyer.objects.filter(token_web=request.session.get('token'))
    goods = Goods.objects.all()
    random_list = goods if len(goods) < 5 else random.sample(goods, 5)
    others_list_first = Collect.objects.all()
    others_list = set()
    for i in range(len(others_list_first)):
        others_list.add(random.choice(others_list_first).goods)
        if len(others_list) == 5:
            break
    response['len_random'] = len(random_list)
    if len(random_list) != 0:
        colle_dic = []
        response['response'] = 1
        for foo in random_list:
            dic = {}
            dic['good'] = get_good_dic_by_model(foo)
            dic['good']['count'] = len(BuyHistory.objects.filter(goods=foo).exclude(state=0))
            dic['store'] = model_to_dict(foo.store)
            colle_dic.insert(0, dic)
        response['random_list'] = colle_dic
    response['len_others'] = len(others_list)
    print len(others_list)
    if len(others_list) != 0:
        colle_dic = []
        response['response'] = 1
        for foo in others_list:
            dic = {}
            dic['good'] = get_good_dic_by_model(foo)
            dic['good']['count'] = len(BuyHistory.objects.filter(goods=foo).exclude(state=0))
            dic['store'] = model_to_dict(foo.store)
            colle_dic.insert(0, dic)
        response['others_list'] = colle_dic
    if len(buyer) == 1:
        user = buyer[0]
        history_list = BuyHistory.objects.all()
        goods_cate = Goods.objects.filter(category=history_list.last().goods.category)
        cate_list = goods_cate if len(goods_cate) < 5 else random.sample(goods_cate, 5)
        if len(cate_list) != 0:
            colle_dic = []
            for foo in cate_list:
                dic = {}
                dic['good'] = get_good_dic_by_model(foo)
                dic['good']['count'] = len(BuyHistory.objects.filter(goods=foo).exclude(state=0))
                dic['store'] = model_to_dict(foo.store)
                colle_dic.insert(0, dic)
            response['cate_list'] = colle_dic
            response['len_cate'] = len(cate_list)
        else:
            pass
        response['response'] = 1
        print response
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        j = json.dumps(response)
        return HttpResponse(j)


def get_report(request):
    response = {'response': '2'}
    error_message = ''
    user = None
    buyer = None
    history_list = []
    history_dic = []
    order_state_list = get_order_state_list()
    print(request.method)
    if request.session.get('token') == '':
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        buyer = Buyer.objects.filter(token_web=request.session.get('token'))
    if len(buyer) == 1:
        user = buyer[0]
        history_list1 = BuyHistory.objects.all()
        for foo in history_list1:
            if foo.goods.store.owner.id == user.id:
                history_list.append(foo)
        response['len'] = len(history_list)
        if len(history_list) != 0:
            for foo in history_list:
                dic = model_to_dict(foo)
                dic['state_text'] = order_state_list[foo.state]
                dic['buyer'] = model_to_dict(foo.buyer)
                dic['good'] = get_good_dic_by_model(foo.goods)
                dic['good']['count'] = len(BuyHistory.objects.filter(goods=foo.goods).exclude(state=0))
                dic['store'] = model_to_dict(foo.goods.store)
                history_dic.insert(0, dic)
            response['history_list'] = history_dic
        else:
            pass
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    print response
    return render_to_response('report.html', locals())


def add_address(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    history_id = ''
    order_id = ''
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        r_platform = req['platform']
        a_name = req['name']
        a_phone = req['phone']
        a_province = req['province']
        a_city = req['city']
        a_county = req['county']
        a_zip = req['zip']
        a_detail = req['detail']
        buyer = Buyer.objects.filter(token=req['token'])
    if len(buyer) == 1:
        user = buyer[0]
        lenA = len(Address.objects.filter(buyer=user))
        address = Address(name=a_name, phone=a_phone, province=a_province, city=a_city, county=a_county,
                          zip=a_zip, detail=a_detail, is_del=0, is_default=(1 if lenA == 0 else 0), buyer=user)
        address.save()
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'no this user'
    response['error_msg'] = error_message
    if r_platform == 'web':
        return HttpResponseRedirect('/info')
    elif r_platform == 'android':
        json.dumps(response)
        j = json.dumps(response)
        return HttpResponse(j)


def get_address_list(request):
    response = {'response': '2'}
    r_platform = 'android'
    error_message = ''
    user = None
    buyer = None
    print(request.method)

    if request.method == 'POST':
        req = json.loads(request.body)
        r_platform = req['platform']
        buyer = Buyer.objects.filter(token=req['token'])

    if len(buyer) == 1:
        user = buyer[0]
        addresses = Address.objects.filter(buyer=user, is_del=0)
        response['len'] = len(addresses)
        if len(addresses) != 0:
            address_dic = []
            for foo in addresses:
                dic = model_to_dict(foo)
                address_dic.insert(0, dic)
            response['address_list'] = address_dic
        else:
            pass
        response['response'] = 1
        print response
    else:
        response['response'] = 2
        error_message = 'error'
    if r_platform == 'web':
        return render_to_response('personal.html', locals())
    elif r_platform == 'android':
        j = json.dumps(response)
        return HttpResponse(j)


def test(request):
    if request.method == 'GET':
        return render_to_response('test.html')
    elif request.method == 'POST':
        return get_goods_by_search(request)


def get_buyer_by_phone(phone_number):
    buyer = Buyer.objects.filter(phone=phone_number)
    print buyer
    return buyer


def get_token(r_password):
    m = hashlib.md5()
    print r_password
    print time.time()
    m.update(r_password + str(time.time()))
    return m.hexdigest()


def get_category():
    c1 = {'10': '手机', '11': '手机配件', '12': '数码相机'}
    c2 = {'20': '板鞋', '21': '跑鞋', '22': '皮鞋'}
    c0 = {'1': c1, '2': c2}
    c_root = {'1': '手机数码', '2': '鞋类', '3': '衣服', '4': '计算机', '5': '零食'}
    print c0
    cMerge = dict(c1, **c2)
    cc = Category(category=c0, root_category=c_root)
    return cc, cMerge


def get_order_state_list():
    return ['未付款', '已付款', '已发货', '待评价', '已评价', '退款中', '已退款', '已关闭']