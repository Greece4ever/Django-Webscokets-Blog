from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class DescriptionImage(models.Model):
    image = models.ImageField()

class Subforum(models.Model):
    name = models.CharField(max_length=100)
    images = models.ManyToManyField(DescriptionImage)

class Categories(models.Model):
    name = models.CharField(max_length=100)
    image = models.ForeignKey(DescriptionImage,null=True,on_delete=models.SET_NULL)

class Article(models.Model):
    # Basic Fields
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    date_created = models.DateTimeField(default=timezone.now)
    
    # Foreign Keys
    images = models.ManyToManyField(DescriptionImage)
    comments = models.ManyToManyField('comment')
    creator = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    forum = models.ForeignKey(Subforum,on_delete=models.CASCADE)

    #Rating
    likes = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="art_likes")
    dislikes = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="art_dislikes")

    #Category
    category = models.ManyToManyField(Categories,related_name='categories')

class comment(models.Model):
    is_reply = models.BooleanField()
    creator = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    reply = models.ManyToManyField("self",related_name='replies')

    #Rating
    likes = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="com_likes")
    dislikes = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="com_dislikes")

class message(models.Model):
    content = models.TextField(max_length=500)

class PrivateMessage(models.Model):
    user_0 = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="receiver")
    user_1 = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="asigner")
    messsages = models.ManyToManyField(message)


class Notification(models.Model):
    TYPES_OF_NOTIFICATIONS = (
        ('C','Comment'),
        ('PM','Private Message'),
    )
    typeof = models.CharField(max_length=2,choices=TYPES_OF_NOTIFICATIONS)
    message = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class UserProfile(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    bio = models.TextField(max_length=500)
    profile_image = models.ImageField()
    followers = models.ManyToManyField(User,blank=True,related_name="followers")
    