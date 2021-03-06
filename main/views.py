from django.shortcuts import render,HttpResponse,Http404,redirect
from django.http import HttpResponseForbidden,JsonResponse,HttpResponseNotFound
from .models import Article,DescriptionImage
import re
import datetime
import json
from PIL import Image
from random import random
import os
from django.conf import settings
from secrets import token_hex
from random import randint

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
    if not user.is_authenticated:
        return redirect("/")
    context = {
        'date' : datetime.datetime.now
    }
    if request.method.lower() == 'get':
        return render(request,"main/create_article.html",context)

    name = request.POST.get("title")
    description = request.POST.get("description")


    if name is None or description is None:
        return JsonResponse({"error" : "Description or title was not received in the request"})

    files = request._get_files()

    if len(files) == 0:
        return JsonResponse({"error" : "There must be at least one image ascosiated with the post"})
    
    usr_id = user.pk

    if len(name) > 200:
        return JsonResponse({"error" : "Title cannot be greater than 200!"})

    if len(description) > 4000:
        return JsonResponse({"error" : "Description cannot be greatear than 4000"})

    # """users/{}/article_images/{}/{}"""

    #Verify that each file is an Image
    file_names = []
    for key in files:
        file = files[key]
        try:
            test_is_valid = Image.open(file)
            test_is_valid.verify()
            file_names.append(str(file))
            assert file.size < 2500000 , "File too big"
        except:
            return JsonResponse({"error" : "Could not identify '{}' as a valid image type or was greater than 2.5 MiB".format(str(file))})
    
    if len(file_names) == 0:
        return JsonResponse({"error" : "You need to provide at least one image"})

    if len(file_names) > 5:
        return JsonResponse({"error" : "Cannot upload more than 5 images in a single Post"})

    #Create the database row
    article = Article(
        creator=user,
        name=name,
        description=description,
    )

    article.save()

    target = os.path.join(settings.BASE_DIR,"external","users","{}".format(user.pk),"article_images",str(article.pk))

    os.makedirs(target)

    thumbnail = request.POST.get("thumbnail")

    print(thumbnail)

    # Iterate over the images and write them
    for key in files:
        file = files[key]
        file_name = str(file)
        if file_names.count(file_name) > 1:
            while file_names.count(file_name) > 1:
                file_name = token_hex(randint(1,10)) # Generate a unique name for that file 
        with open(os.path.join(target,file_name),'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        img = DescriptionImage(creator=user,article=article,image=os.path.join("users","{}".format(user.pk),"article_images",str(article.pk),file_name))
        img.save()
        article.images.add(img)
        if thumbnail == file_name:
            article.thumbnail = img
            article.save()


    if thumbnail is None or thumbnail not in file_names:
        article.thumbnail = article.images.all().first()
        article.save()

    return JsonResponse({"id" : article.pk})

def get_articles(request):
    """
        For handling AJAX request from articles
    """
    if request.method.lower() != 'get':
        return(HttpResponseForbidden("Invalid Permissiosn"))
    print(request.headers)
    articles = request.headers.get("Articles")
    articles = json.loads(articles)
    ArticleArray = {"success" : []}
    for article in articles:
        article = Article.objects.filter(pk=article).first()
        if article is None:
            continue
        ArticleArray['success'].append({
            "id" : article.pk,
            "name" :  article.name,
            "description" : article.description if len(article.description) < 600 else article.description[:600],
            "likes" : article.likes.all().count(),
            "user" : article.creator.userprofile.nickname,
            "img_user" : article.creator.userprofile.profile_image.url,
            "image" : article.thumbnail.image.url,
            "date_created" : article.date_created.strftime('%A %d %B %Y')
        })

    return JsonResponse(ArticleArray)


def RemoveArticleView(request,id):
    user = request.user
    article = Article.objects.filter(pk=id).first()
    if article is None:
        return HttpResponseForbidden("Cannot delete something that doesn't exist")
    if article.creator != user:
        return HttpResponseForbidden("Cannot delete someone else's post!")
    article.delete()
    return redirect("/")