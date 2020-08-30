from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

def max_file_size(file_value):
    max_length = 3 * 1048576 #2.5 MiB
    if file_value.size > max_length:
        raise ValidationError('File cannot be greater than 3 MiB')

def article_image(instance,filename):
    return 'users/{}/article_images/{}/{}'.format(instance.creator.id,instance.id,filename)

def profile_image(instance,filename):
    return 'users/{}/profiles/{}/{}'.format(instance.owner.id,instance.id,filename)

def sub_forums(instance,filename):
    return 'forums/{}/description/{}'.format(instance.id,filename)

def categories(instance,filename):
    return 'forums/categories/{}/{}'.format(instance.id,filename)

class ProfileQueryset(models.QuerySet):

    def delete(self,*args,**kwargs):
        for instance in self:
            instance.profile_image.delete()
        super(ProfileQueryset, self).delete(*args, **kwargs)


class DescriptionImage(models.Model):
    image = models.ImageField(upload_to=article_image,validators=[max_file_size])
    creator = models.ForeignKey(User,related_name="image_uploader",null=True,on_delete=models.SET_NULL)
    article = models.ForeignKey("Article",related_name="parent",on_delete=models.CASCADE,null=True)
    

    def __str__(self):
        return f'Image at {self.article}'

# 1 Image
class Subforum(models.Model):
    name = models.CharField(max_length=100)
    images = models.ImageField(upload_to=sub_forums,validators=[max_file_size],null=True)

    def __str__(self):
        return f'{self.name}'

# 1 Image
class Categories(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=categories,validators=[max_file_size],null=True)

# Multiple Images
class Article(models.Model):
    # Basic Fields
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    date_created = models.DateTimeField(default=timezone.now)
    
    # Foreign Keys
    images = models.ManyToManyField(DescriptionImage,related_name="imgres",blank=True)
    comments = models.ManyToManyField('comment',blank=True)
    creator = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    forum = models.ForeignKey(Subforum,on_delete=models.CASCADE,null=True,default=None)

    #Rating
    views = models.IntegerField(default=0)
    likes = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="art_likes",blank=True)
    dislikes = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="art_dislikes",blank=True)

    #Category
    category = models.ManyToManyField(Categories,related_name='categories',blank=True)


    def __str__(self):
        return f'"{self.name}" by "{self.creator.username}"'

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

# 1 Image
class UserProfile(models.Model):
    objects = ProfileQueryset.as_manager()
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    bio = models.TextField(max_length=500)
    profile_image = models.ImageField(upload_to=profile_image,validators=[max_file_size])
    followers = models.ManyToManyField(User,blank=True,related_name="followers")
    public = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.owner.username}'