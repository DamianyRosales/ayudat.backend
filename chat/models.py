from django.db import models

# Create your models here.

class Conversation(models.Model):

    conversationID = models.CharField(db_column='conversationID', max_length=255,unique=True)
    messages = models.TextField(db_column='messages', default='')

    def __str__(self):
        return self.conversationID