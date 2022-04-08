# Generated by Django 4.0.3 on 2022-04-08 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversationID', models.CharField(db_column='conversationID', max_length=255, unique=True)),
                ('messages', models.TextField(db_column='messages')),
            ],
        ),
    ]
