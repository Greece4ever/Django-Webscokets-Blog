from django.contrib import admin
from .models import Article,DescriptionImage,UserProfile,Subforum

# Register your models here.

admin.site.register(Article)
admin.site.register(DescriptionImage)
admin.site.register(UserProfile)
admin.site.register(Subforum)
