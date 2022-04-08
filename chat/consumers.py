# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .views import conversation_view

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        

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
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

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