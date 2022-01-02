from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .dic import WeblioDic, GogenyuraiDic

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    weblio = WeblioDic()
    weblio_de = weblio.search('ほし')
    gogen = GogenyuraiDic()
    gogen_de = gogen.search('ほし')

    context = {
        'host_url': 'http://localhost:8000/',
        'dics': [weblio_de, gogen_de],
    }
    return render(request, 'index.html', context=context)
