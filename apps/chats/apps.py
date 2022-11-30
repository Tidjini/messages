from django.apps.config import AppConfig


class ChatsConfig(AppConfig):
    name = "apps.chats"
    verbose_name = "Chats Application"

    def ready(self):
        from . import signals
