from django.apps import AppConfig


class ChatsConfig(AppConfig):

    name = "apps.chats"
    verbose_name = "Chats Applications"

    def ready(self):
        from . import signals
