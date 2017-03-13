"""
Consumers define function for websocket connecting, receiving messages
and disconnecting.
"""
from channels.generic.websockets import JsonWebsocketConsumer
from django.shortcuts import get_object_or_404

from backpage.models import User

class PositionsConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def get_object(self, pk, token):
        """Get object and check the permissions of user."""
        try:
            if pk is None or token is None:
                return None

            obj = User.objects.get(pk=pk)

            if token != obj.id.token:
                return None
            else:
                return obj

        except Exception:
            return None

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        pk = kwargs.get("pk", None)
        token = kwargs.get("token", None)

        obj = self.get_object(pk, token)

        if obj is None:
            message.reply_channel.send({"accept": False})
            self.close()

        print(message.reply_channel)

    def receive(self, content, **kwargs):
        """
        ASGI WebSocket packet-received and send-packet message types
        both have a "text" key for their textual data.
        """
        print(content['web'])
        self.send(content)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        print(message.reply_channel)
