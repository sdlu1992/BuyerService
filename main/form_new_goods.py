# coding=utf-8
__author__ = 'sdlu'

import django.forms as forms


class NewGoodForm(forms.Form):
    good_name = forms.CharField()
    good_price = forms.IntegerField()
