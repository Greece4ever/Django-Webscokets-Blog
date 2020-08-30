import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Article,User

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
