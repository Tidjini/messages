# Generated by Django 4.1.3 on 2022-11-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0002_discussion_message_participant_messagevue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discussion",
            name="type",
            field=models.CharField(
                choices=[("s", "single"), ("g", "group")], default="s", max_length=1
            ),
        ),
    ]
