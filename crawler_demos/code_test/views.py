from django.shortcuts import render
from common import utils

# Create your views here.
def hello(request):
    return render(request, "hello.html")


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
