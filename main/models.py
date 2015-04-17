#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

import sys

print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

class Buyer(models.Model):
    # user = models.OneToOneField(User)
    nickname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    credit = models.IntegerField()
    credit_id = models.CharField(max_length=18)
    type = models.IntegerField()
    birthday = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    name = models.CharField(max_length=20)
    token = models.CharField(max_length=50)
    token_web = models.CharField(max_length=50)
    address = models.CharField(max_length=500)

    def __unicode__(self):
        return self.phone


class Store(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(Buyer)
    address = models.CharField(max_length=100)
    credit = models.IntegerField()

    def __unicode__(self):
        return self.name


class Goods(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    store = models.ForeignKey(Store)
    category = models.IntegerField()
    des = models.CharField(max_length=2000)
    image_url_title = models.CharField(max_length=200)
    image_url_other = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    buyer = models.ForeignKey(Buyer)
    goods = models.CharField(max_length=1000)
    date = models.CharField(max_length=30)
    state = models.IntegerField()
    price = models.FloatField()

    def __unicode__(self):
        return self.goods.name


# state=0 未付款
# state=1 已付款
# state=2 已发货
# state=3 确认收货
# state=4 申请退款
# state=5 已退款
# state=-1 已关闭
class BuyHistory(models.Model):
    buyer = models.ForeignKey(Buyer)
    goods = models.ForeignKey(Goods)
    date = models.CharField(max_length=30)
    price = models.FloatField()
    amount = models.IntegerField()
    order = models.ForeignKey(Order)
    state = models.IntegerField()

    def __unicode__(self):
        return self.goods.name


class Appraise(models.Model):
    type = models.IntegerField()
    buy_history = models.OneToOneField(BuyHistory)
    content = models.CharField(max_length=500)
    data = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id


class Category(models.Model):
    category = models.CharField(max_length=2000)
    root_category = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id


class WishList(models.Model):
    goods = models.ForeignKey(Goods)
    buyer = models.ForeignKey(Buyer)
    amount = models.IntegerField()
    date = models.CharField(max_length=30)

    def __unicode__(self):
        return self.id


class Collect(models.Model):
    goods = models.ForeignKey(Goods)
    buyer = models.ForeignKey(Buyer)

    def __unicode__(self):
        return self.id