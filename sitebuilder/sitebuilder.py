#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-05 22:16:32
# @Author  : warlock921 (you@example.org)
# @Link    : http://1981tec.com
# @Version : $Id$

import sys
import os

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY','q8zm+76ay4q-3bazogfq0j04534gmpnm5(o)rdw8)nzr@9jmzm')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

settings.configure(
	DEBUG = DEBUG,
	SECRET_KEY = SECRET_KEY,
	ALLOWED_HOSTS = ALLOWED_HOSTS,
	ROOT_URLCONF = 'urls',
	MIDDLEWARE_CLASSES = (),
	INSTALLED_APPS = (
		'django.contrib.staticfiles',
		'sitebuilder',

	),
	TEMPLATES = (

		{
			'BACKEND':'django.template.backends.django.DjangoTemplates',
			'DIRS':[],
			'APP_DIRS':True,
		},

	),
	STATIC_URL = '/static/',
	SITE_PAGES_DIRECTORY = os.path.join(BASE_DIR,'pages'),
	SITE_OUTPUT_DIRECTORY = os.path.join(BASE_DIR,'_build'),
	STATIC_ROOT = os.path.join(BASE_DIR,'_build','static'),
)


if __name__ == '__main__':
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)