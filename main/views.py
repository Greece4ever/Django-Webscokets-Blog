from django.shortcuts import render,HttpResponse,Http404,redirect
from .models import Article
import re
import datetime

# Create your views here.


def index(request):
    context = {"articles" : Article.objects.all()}
    return render(request,"main/index.html",context)

def detail_article(request,name):
    id = name.split("-")[-1]   
    try:
        if Article.objects.filter(pk=id).exists():
            context = {
                'article' : Article.objects.filter(pk=id).first()
            }
            return render(request,"main/detail.html",context)
    except:
        pass
    raise Http404("Not found")


def article_create(request):
    user = request.user
    if not request.user:
        return redirect("/")
    context = {
        'date' : datetime.datetime.now
    }
    return render(request,"main/create_article.html",context)