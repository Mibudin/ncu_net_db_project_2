from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from .dic import WeblioDic, GogenyuraiDic, DicEntry
from .forms import SearchDicForm
from .models import QueryRecord

# Create your views here.


_weblio = WeblioDic()
_gogen = GogenyuraiDic()


def index(request: HttpRequest, query: str) -> HttpResponse:
    dics: list[DicEntry] = []
    if request.method == 'POST':
        form = SearchDicForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('index', kwargs={'query': form.cleaned_data['query']}))

    else:
        form = SearchDicForm(initial={'query': query})

        if query:
            QueryRecord(query=query).save()
            dics += _weblio.search(query)
            dics += _gogen.search(query)

    context = {
        'query': query,
        'form': form,
        'host_url': settings.HOST_URL,
        'dics': dics,
    }

    return render(request, 'index.html', context=context)
