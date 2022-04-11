import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models import Conversation


class ChatConsumer(AsyncWebsocketConsumer):

    def createConversationID(self, room_name):
        if not Conversation.objects.filter(conversationID=room_name).exists():
            Conversation.objects.create(conversationID=room_name)

    def putMessages(self, room_name, message):
        try:
            conversation = Conversation.objects.get(conversationID=room_name)

            conversation.messages = conversation.messages + \
                str(message) + '░███§¥╩»»██'
            conversation.save()
        except:
            print('******** Conversation exists')

    def get_messages(self, room_name):
        try:
            conversation = Conversation.objects.get(conversationID=room_name)
            messages = conversation.messages.split('░███§¥╩»»██')
            return messages
        except:
            pass

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await database_sync_to_async(self.createConversationID)(self.room_name)

        # typeFront !== 'chat_started'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.messages = await database_sync_to_async(self.get_messages)(self.room_name)
        msgSend = self.messages
        if self.messages == '': 
            msgSend = []
        await self.send(text_data=json.dumps({
            'typeFront': 'chat_started',
            'messages': msgSend
        }))
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await database_sync_to_async(self.putMessages)(self.room_name, text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'typeFront': 'chat_started',
                'data': text_data_json
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'typeFront': 'chat_message',
            'for': event['data']['for'],
            'from': event['data']['from'],
            'content': event['data']['content'],
            'time': event['data']['time'],
        }))