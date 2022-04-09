# chat/consumers.py
import json
from os import lseek
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.views import conversation_view
from chat.models import Conversation
import requests

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

        url = 'https://127.0.0.0:8000/chat/conversation/'
        conversationID = {
            'conversationID': self.room_name,
        }

        if Conversation.objects.filter(conversationID=self.room_name).exists():
            pass
            # requests.post(url,data=conversationID)
            # conversation_view.post(conversationID)
        # else:
        #     conversation_view.put()

        # TODO: Request to get messages from database of both users
        # angi_ed01@hotmail.comdamiany@hotmail.com
        self.send(text_data=json.dumps({
             'conversationId': 'angi_ed01@hotmail.comdamiany@hotmail.com',
             'messages': [
                
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
        print(text_data)

        text_data_json = json.loads(text_data)
        
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'for': text_data_json['for'],
            'from': text_data_json['from'],
            'content': text_data_json['content'],
            'time': text_data_json['time'],
            'channel': self.room_name
        }))

    # # TODO: Upload messages to database

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))