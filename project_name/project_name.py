#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-05 22:16:32
# @Author  : warlock921 (you@example.org)
# @Link    : http://1981tec.com
# @Version : $Id$

import sys
import os

from django.conf.urls import url
from django.http import HttpResponse

from django.conf import settings

from django.core.wsgi import get_wsgi_application


DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY','{{secret_key}}')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

def index(request):
	return HttpResponse('恭喜，成功开启了你的Django之旅 !')

urlpatterns = (
	url(r'^$',index),
)

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
)

application = get_wsgi_application()

if __name__ == '__main__':
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)