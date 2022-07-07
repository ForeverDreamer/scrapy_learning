# from django.http import HttpResponse
from django.shortcuts import render


def welcome(request):
    return render(request, "index/welcome.html")
    # return HttpResponse("你好, 欢迎来到爬虫宇宙!")
