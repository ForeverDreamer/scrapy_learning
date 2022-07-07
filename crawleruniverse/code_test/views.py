from django.shortcuts import render
from common import utils
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
import sys
import logging


def init_logger():
    tmp_logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
    stream_handler.setFormatter(formatter)
    tmp_logger.addHandler(stream_handler)
    tmp_logger.setLevel(logging.DEBUG)

    return tmp_logger


logger = init_logger()


# Create your views here.
def request_info(request):
    scheme = request.scheme
    body = request.body
    path = request.path
    method = request.method
    host = request.get_host()
    get = request.GET
    post = request.POST
    cookies = request.COOKIES
    http_x_forwarded_for, remote_addr, client_ip = utils.get_ip_address(request)
    remote_host = request.META.get("REMOTE_HOST", "")
    # meta = request.META
    headers = request.headers

    return render(request, "request_info.html", locals())


ip_count = {}
@cache_page(0)
def proxy_server(request):
    ip = request.META.get("REMOTE_ADDR")
    if ip in ip_count.keys():
        ip_count[ip] += 1
    else:
        ip_count[ip] = 1

    logger.info(ip_count)
    if ip_count[ip] > 5:
        return HttpResponseForbidden("banned")
    else:
        return JsonResponse({"ip": ip, "count": ip_count[ip]})


