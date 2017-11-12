import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
from django.utils._os import safe_join

def get_page_or_404(name):
	"""  使用Django模板技术返回页面地址或者抛出404错误 """

	try:
		file_path = safe_join(settings.SITE_PAGES_DIRECTORY,name)
	except ValueError:
		raise Http404('Page Not Found')
	else:
		if not os.path.exists(file_path):
			raise Http404('Page not Found')
	with open(file_path,'r') as f:
		page = Template(f.read())
	
	return page

def page(request,slug='index'):
	"""如果找到请求页面就渲染它"""

	#这个字典用于显示页面的名称，也就是标题，在这里配置后，不用定义base.html的<title>标签了
	slug_tmp = {'index':'首页','contact':'联系我们','news':'新闻','login':'登录页'}
	
	file_name = '{}.html'.format(slug)
	page = get_page_or_404(file_name)
	#这里是传到页面的值，哪里想用都可以用
	context = {
		'slug_tmp':slug_tmp[slug],
		'slug':slug,
		'page':page,
	}

	return render(request,'page.html',context)