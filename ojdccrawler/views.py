from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .dic import WeblioDic, GogenyuraiDic
from .forms import SearchDicForm

# Create your views here.


def index(request: HttpRequest, q: str) -> HttpResponse:
    if request.method == 'POST':
        form = SearchDicForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('index', kwargs={'q': form.cleaned_data['query']}))

    else:
        form = SearchDicForm(initial={'query': q})

        weblio = WeblioDic()
        weblio_de = weblio.search(q)
        gogen = GogenyuraiDic()
        gogen_de = gogen.search(q)

    context = {
        'form': form,
        'host_url': 'http://localhost:8000/',
        'dics': [weblio_de, gogen_de],
    }

    return render(request, 'index.html', context=context)
