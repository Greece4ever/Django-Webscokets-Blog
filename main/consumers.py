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
        print("RECEVEID DATA")
        print(self.is_authenticated)
        if not self.is_authenticated:
            print("NOT AUTHENTICATED")
            self.disconnect()
            return None
        data = json.loads(text_data)
        print(data)
        if data['data'].strip() != '':
            print("data is not none")
            if data['type'] == 'comment':
                print("comment")
                if data['is_reply']:
                    print("reply")
                    parent = comment.objects.filter(id=data['parent'])
                    if parent.exists() and self.article.comments.filter(id=parent.first().pk):
                        parent = parent.first()
                    else:
                        print("parrent does not exists")
                        return None

                com = comment(creator=self.user,description=data['data'],is_reply=data['is_reply'])
                com.save()
                self.article.comments.add(com)
                if data['is_reply']:
                    parent.reply.add(com)
                    
                async_to_sync(self.channel_layer.group_send)(
                    self.connection,
                    {
                        'type' : 'comment',
                        'message' : {
                            'img' : self.user.userprofile.profile_image.url,
                            'name' : self.user.userprofile.nickname,
                            'id' : com.pk,
                            'msg' : com.description,
                            'date_created' : f'{com.date_created.year}/{com.date_created.month}/{com.date_created.day} - {com.date_created.hour}/{com.date_created.minute}/{com.date_created.second}',
                            'is_reply' : data['is_reply'],
                            'parent_id' : parent.pk if data['is_reply'] else None
                        }
                    }
                )

    def comment(self,event):
        msg = event['message']
        msg = json.dumps(msg)
        print(msg)
        self.send(msg)
    