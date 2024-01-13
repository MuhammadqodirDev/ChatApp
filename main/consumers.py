import json
from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import CustomUser, Chat, Message
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            user = self.scope["user"]
        else:
            print(self.scope.get("query_string"))
            query = parse_qs(self.scope.get("query_string").decode("utf-8"))

            token = query.get('token')[0]

            # Authenticate the user using the token
            user = await self.get_user_from_token(token)


        if user and user.is_authenticated:
                # If authentication is successful, accept the WebSocket connection
            await self.accept()
            self.user = user

            chats = await self.get_user_chats(user) 
            await self.add_user_to_chats(user, chats)
            for chat in chats:
                await self.channel_layer.group_add(chat.chat_name, self.channel_name)


        else:
            # If authentication fails, close the WebSocket connection
            await self.close()




    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        user = self.user
        chat = await self.get_chat(text_data_json)


        res = await self.create_message(chat, user, message)
        
        if res:
            await self.channel_layer.group_add(chat.chat_name, self.channel_name)
            await self.channel_layer.group_send(
                chat.chat_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "chat_name": chat.chat_name,
                },
            )


    @database_sync_to_async
    def get_chat(self, text_data, chat_id=None):
        if not chat_id:
            chat_id = text_data['kwargs']['chat_id']
        chat, created = Chat.objects.get_or_create(id=chat_id)
        return chat
    
    @database_sync_to_async
    def create_message(self, chat, sender, text):
        if sender in chat.participants.all():
            message = Message.objects.create(chat=chat, sender=sender, text=text)
            message.save()
            return message
        return

    

    @database_sync_to_async
    def get_user_chats(self, user):
        # Retrieve all chats for the user
        return Chat.objects.filter(participants=user)
    
    @database_sync_to_async
    def add_user_to_chats(self, user, chats):
        for chat in chats:
            # await self.channel_layer.group_add(chat.chat_name, self.channel_name)
            chat.participants.add(user)


    @database_sync_to_async
    def get_user_from_token(self, token):
        # Retrieve the user associated with the token
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

    async def chat_message(self, event):
        message = event['message']
        chat_name = event['chat_name']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'chat_name': chat_name,
        }))

    


