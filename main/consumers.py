import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Article,User,comment

class ArticleConsumer(WebsocketConsumer):
    def connect(self):

        self.connection = "articles"
        
        async_to_sync(self.channel_layer.group_add)(
            self.connection,
            self.channel_name
        )

        self.accept()

    def receive(self,text_data):        
        data = json.loads(text_data)
        usr = User.objects.filter(username=self.scope["user"]).first()
        article = Article.objects.filter(pk=int(data['article_id'])).first()


        if article.likes.filter(username=usr.username).exists():
            print("removing like")
            article.likes.remove(usr)
        else:
            print("adding like")
            article.likes.add(usr)

        if data['type'] == "vote":
            pass
        async_to_sync(self.channel_layer.group_send)(
            self.connection,
            {
                'type': 'vote',
                'message': {
                    "type" : "vote",
                    "id" : article.pk,
                    "likes" : article.likes.all().count(),
                }
            }
        )

    def vote(self,event):
        message = json.dumps(event['message'])
        self.send(message)

class ArticleDetailConsumer(WebsocketConsumer):

    def connect(self):  
        ids = [item for item in self.scope['path'].split("/") if item.strip() != ''][-1]
        article = Article.objects.filter(pk=ids)
        self.is_authenticated = self.scope['user'].is_authenticated

        if self.is_authenticated:
            self.user = User.objects.filter(username=self.scope["user"]).first()

        if article.exists(): 
            print("Row detected in database")
            self.connection = "art_{}".format(ids)
            self.article = article.first()
            async_to_sync(self.channel_layer.group_add)(
                self.connection,
                self.channel_name
            )
            self.accept()
    
    def receive(self,text_data):
        if not self.is_authenticated:
            self.disconnect()
            return None
        data = json.loads(text_data)
        if data['data'].strip() != '':
            if data['type'] == 'comment':
                com = comment(creator=self.user,description=data['data'],is_reply=data['is_reply'])
                com.save()
                self.article.comments.add(com)
                async_to_sync(self.channel_layer.group_send)(
                    self.connection,
                    {
                        'type' : 'comment',
                        'message' : {
                            'img' : self.user.userprofile.image,
                            'msg' : com.description,
                            'date_created' : com.date_created
                        }
                    }
                )

    def comment(self,event):
        msg = event['message']
        self.send(msg)
    