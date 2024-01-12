import json
from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import CustomUser, Chat, Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # kwargs = text_data_json.get('kwargs')

        # if not kwargs:
        #     return
        
        user = self.scope['user']
        chat = await self.get_chat(text_data)


        message = await self.create_message(chat, user, message)

        
        await self.channel_layer.group_add("chat", chat.chat_name)
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat.message",
                "message": message,
            },
        )


    @database_sync_to_async
    def get_chat(self, text_data):
        chat, created = Chat.objects.get_or_create(is_group_chat=True)
        return chat
    
    @database_sync_to_async
    def create_message(self, chat, sender, text):
        message = Message.objects.create(chat=chat, sender=sender, text=text)
        message.save()
        return message


    async def chat_message(self, event):
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({'message': message}))

