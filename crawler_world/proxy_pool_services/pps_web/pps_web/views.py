from django.http import JsonResponse
from django.http import HttpResponse
from config.config_getter import config
from util.proxy_manager import ProxyManager


def welcome(request):
    return JsonResponse(config.get_api_list)


def get(request):
    proxy = ProxyManager().get()
    return HttpResponse(proxy) if proxy else HttpResponse('暂无可用代理!')


def get_all(request):
    proxies = ProxyManager().get_all()
    return HttpResponse(proxies) if proxies else HttpResponse('暂无可用代理!')


def delete(request):
    proxy = request.GET.get('proxy')
    if proxy:
        ProxyManager().delete(proxy)
        return HttpResponse('删除{}成功！'.format(proxy))
    else:
        return HttpResponse('请指定要删除的代理ip！')


def get_status(request):
    status = ProxyManager().get_number()
    return JsonResponse(status)
