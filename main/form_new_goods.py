# coding=utf-8
__author__ = 'sdlu'

import django.forms as forms


class NewGoodForm(forms.Form):
    goods_name = forms.CharField()
    price = forms.CharField()
    root_category = forms.CharField()
    category = forms.CharField()
    image_title = forms.FileField()
    image1 = forms.FileField(required=False)
    image2 = forms.FileField(required=False)
    image3 = forms.FileField(required=False)
    image4 = forms.FileField(required=False)
