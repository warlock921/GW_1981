#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-05 22:16:32
# @Author  : warlock921 (you@example.org)
# @Link    : http://1981tec.com
# @Version : $1.0$

#文件头导入部分
import sys
import os
import hashlib

from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
from django.conf import settings


from django.conf.urls import url
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse,HttpResponseBadRequest
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render
from django.views.decorators.http import etag


#setting部分
DEBUG = os.environ.get('DEBUG','on') == 'on'
#随机生成的SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY','1*wp@2t@bpuqocm1tt=!kij*^%-htjj+83fx^gits@u9*fgw7s')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

BASE_DIR = os.path.dirname(__file__)

settings.configure(
	DEBUG = DEBUG,
	SECRET_KEY = SECRET_KEY,
	ALLOWED_HOSTS = ALLOWED_HOSTS,
	ROOT_URLCONF = __name__,
	MIDDLEWARE_CLASSES = (
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	),
	INSTALLED_APPS = (
		'django.contrib.staticfiles',
	),
	TEMPLATES = (
		{
			'BACKEND':'django.template.backends.django.DjangoTemplates',
			'DIRS':(os.path.join(BASE_DIR,'templates'),)
		},
	),
	STATICFILES_DIRS = (
		os.path.join(BASE_DIR,'static'),
	),
	STATIC_URL = '/static/',

)


#models模型部分
class ImageForm(forms.Form):
	height = forms.IntegerField(min_value=1,max_value=2000)
	width = forms.IntegerField(min_value=1,max_value=2000)
	
	#封装图片信息的函数
	def generate(self,image_format='PNG'):
		height = self.cleaned_data['height']
		width = self.cleaned_data['width']
		#加入缓存
		key = '{}.{}.{}'.format(width,height,image_format)
		content = cache.get(key)
		if content is None:
			#使用Pillow创建图片
			image = Image.new("RGB",[width,height],"#ccc")
			#为黑底图片加入图片信息
			draw = ImageDraw.Draw(image)
			text = '{} X {}'.format(width,height)
			textwidth,textheight = draw.textsize(text)
			if textwidth < width and textheight < height:
				texttop = (height - textheight) // 2
				textleft = (width - textwidth) // 2
				draw.text((textleft,texttop),text,fill=(255,255,255))
			#将图片转化为Bytes流
			content = BytesIO()
			image.save(content,image_format)
			content.seek(0)
			#当未找到缓存图片且创建了新图片时，通过键值将图片在缓存保存一小时
			cache.set(key,content,60 * 60)
		return content

def generate_etag(request,width,height):
	content = 'Placeholder:{0} x {1}'.format(width,height)
	return hashlib.sha1(content.encode('utf-8')).hexdigest()

#view 视图部分
'''修饰函数，创建浏览器缓存'''
@etag(generate_etag)
def placeholder(request,width,height):
	form = ImageForm({'height':height,'width':width})
	if form.is_valid():
		image = form.generate()
		height = form.cleaned_data['height']
		width = form.cleaned_data['width']
		return HttpResponse(image,content_type='image/png')
	else:
		return HttpResponseBadRequest('Ivalid Image Request')

def index(request):
	example = reverse('placeholder',kwargs={'width':50,'height':50})
	context = {
		'example':request.build_absolute_uri(example)
	}
	return render(request,'home.html',context)

#url路由部分
urlpatterns = (
	url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',placeholder,name='placeholder'),
	url(r'^$',index,name='homepage'),
)

#服务器接口--从这里启动

application = get_wsgi_application()

if __name__ == '__main__':
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)