# chat/consumers.py
import json
from os import lseek
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.views import conversation_view
from chat.models import Conversation

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.accept()

        print('Client connected')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        conversationID = {
            'conversationID': self.room_name,
        }

        # if not Conversation.objects.filter(conversationID=self.room_name).exists():
        #     conversation_view.post(conversationID)
        # else:
        #     conversation_view.put()

        self.send(text_data=json.dumps({
            'caca':self.room_name
        }))
        # TODO: Request to get messages from database of both users
        # angi_ed01@hotmail.comdamiany@hotmail.com
        self.send(text_data=json.dumps({
             'conversationId': 'angi_ed01@hotmail.comdamiany@hotmail.com',
             'messages': [
                {
                    'id': 1, 
                    'content': 'Hola',
                    'time': '10:00 am',
                    'sender': 0
                },
                {
                    'id': 2,
                    'content': 'CACOTA',
                    'time': '10:00 am',
                    'sender': 1
                }

            ]
        }))



        # Join room group
      

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

    # TODO: Upload messages to database

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))