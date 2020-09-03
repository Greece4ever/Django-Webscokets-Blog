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
        if 'key' in data:
            async_to_sync(self.channel_layer.group_send)(
                self.connection,
                {
                    'type': 'vote',
                    'message': {
                        "type" : "new_post",
                        "id" : data['id'],
                    }
                }
            )
            print("SENDING DATA")
            return -1

        usr = User.objects.filter(username=self.scope["user"]).first()
        article = Article.objects.filter(pk=int(data['article_id'])).first()
        print("RECEVED DATA")

        if article.likes.filter(username=usr.username).exists():
            article.likes.remove(usr)
        else:
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

    def new_post(self,event):
        print("DISPATCH")
        return self.vote(event)


def handleRating(connection,groups,specific,id,likes,dislikes):
    async_to_sync(groups)(
        connection,
        {
            'type': 'vote',
            'message': {
                "type" : "vote",
                "specific" : specific,
                "id" : id,
                "likes" : likes,
                "dislikes" : dislikes
            }
        }
    )

class ArticleDetailConsumer(WebsocketConsumer):

    def connect(self):  
        ids = [item for item in self.scope['path'].split("/") if item.strip() != ''][-1]
        article = Article.objects.filter(pk=ids)
        self.user = self.scope['user']
        self.is_authenticated = self.scope['user'].is_authenticated
        self.article = article

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
                if data['is_reply']: #handle reply
                    parent = comment.objects.filter(id=data['parent'])
                    if parent.exists() and self.article.comments.filter(id=parent.first().pk):
                        parent = parent.first()
                    else:
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
                            'type' : "comment",
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
            elif data['type'] == 'rate': #handle rating
                if data['specific'] == 'article':
                    #rating on the article
                    if data['vote'] == 'dislike': #handle dislike
                        #handle dislike
                        if self.article.dislikes.filter(username=self.user.username).exists():
                            self.article.dislikes.remove(self.user)
                        else:
                            if self.article.likes.filter(username=self.user.username).exists():
                                self.article.likes.remove(self.user)
                            self.article.dislikes.add(self.user)
                    elif data['vote'] == 'like': #handle like
                        #handle like
                        if self.article.likes.filter(username=self.user.username).exists():
                            self.article.likes.remove(self.user)
                        else:
                            if self.article.dislikes.filter(username=self.user.username).exists():
                                self.article.dislikes.remove(self.user)
                            self.article.likes.add(self.user)
                    handleRating(self.connection,self.channel_layer.group_send,"article",self.article.pk,likes=self.article.likes.all().count(),dislikes=self.article.dislikes.all().count())
                    return -1
                else: 
                    com_id = data['id']
                    com = comment.objects.filter(pk=com_id).first()
                    if com is None:
                        self.disconnect()
                        print("DISCONNECTED BECAUSE COMMENT WAS NOT FOUND")
                        return None

                    if data['vote'] == 'dislike':
                        if com.dislikes.filter(username=self.user.username).exists():
                            com.dislikes.remove(self.user)
                        else:
                            com.dislikes.add(self.user)

                    elif data['vote'] == 'like':
                        #handle like
                        if com.likes.filter(username=self.user.username).exists():
                            com.likes.remove(self.user)
                        else:
                            com.likes.add(self.user)
                    #Send the socket
                    handleRating(self.connection,self.channel_layer.group_send,"comment",com.pk,likes=com.likes.all().count(),dislikes=com.dislikes.all().count())


    def comment(self,event):
        msg = event['message']
        msg = json.dumps(msg)
        print(msg)
        self.send(msg)
    
    def vote(self,event):
        return self.comment(event)