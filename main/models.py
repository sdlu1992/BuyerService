from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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

    def __unicode__(self):
        return self.name


class BuyHistory(models.Model):
    buyer = models.ForeignKey(Buyer)
    goods = models.ForeignKey(Goods)
    date = models.CharField(max_length=30)
    state = models.IntegerField()
    price = models.FloatField()
    amount = models.IntegerField()

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