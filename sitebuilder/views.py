import os
import json

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template,Context
from django.template.loader_tags import BlockNode
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

	#遍历页面的原始节点列表，检查名称为context的BlockNode,也就是找到名为context的{% block %}块，它会定义一个元变量供我们包含内容
	meta = None
	for i,node in enumerate(list(page.nodelist)):
		if isinstance(node,BlockNode) and node.name == 'context':
			meta = page.nodelist.pop(i)
			break
	page._meta = meta
	return page

def page(request,slug='index'):
	"""如果找到请求页面就渲染它"""

	#这个字典用于显示页面的名称，也就是标题，在这里配置后，不用定义base.html的<title>标签了
	slug_tmp = {'index':'首页','contact':'联系我们','news':'新闻','login':'登录页','pricing':'价格查询'}
	#然后将要渲染的页面名称进行组合
	file_name = '{}.html'.format(slug)
	page = get_page_or_404(file_name)
	#这里是传到页面的值，被传值的页面使用{{slug}}来引用，很灵活
	context = {
		'slug_tmp':slug_tmp[slug],
		'slug':slug,
		'page':page,
	}
	#元数据上下文通过Python的json模块来渲染,将{% block content %}转换成可理解的Python
	if page._meta is not None:
		meta = page._meta.render(Context())
		extra_context = json.loads(meta)
		context.update(extra_context)
	return render(request,'page.html',context)