from django.shortcuts import render,HttpResponse,Http404,redirect
from django.http import HttpResponseForbidden,JsonResponse
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
            print("Changing thumbnail")
            article.thumbnail = img
            print(article.thumbnail)


    if thumbnail is None or thumbnail not in file_names:
        print("Changing thumbnail")
        article.thumbnail = article.images.all().first()
        article.thumbnail.save()
        print(article.thumbnail)

    return JsonResponse({"id" : article.pk})