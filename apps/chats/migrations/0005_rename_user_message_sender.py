# Generated by Django 4.1.3 on 2022-12-02 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0004_rename_utilisateur_message_user_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="user",
            new_name="sender",
        ),
    ]
