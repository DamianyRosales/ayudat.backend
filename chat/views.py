from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView

from users_api import serializers
from .serializers import ConversationSerializer
from rest_framework import status

import json

from . import models# Create your views here.
from rest_framework import permissions

def lobby(request, room_name):
    return JsonResponse(data={'Channel': 'Angel es popo'})

class conversation_view(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self,request, format=None):
        conversationID = request.data.get('conversationID')
        conversation = models.Conversation.objects.get(conversationID=conversationID)
        serializer = ConversationSerializer(conversation, many=False)
        return JsonResponse(data=serializer.data, safe = False)


    def put(self, request):
        data = json.loads(json.dumps(request.data))

        conversation = models.Conversation.objects.get(
            conversationID = request.data.get('conversationID')
            )
        
        serializer = ConversationSerializer(conversation, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = json.loads(json.dumps(request.data))
        serializer = ConversationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        try:
            conversation = models.Conversation.objects.get(
                conversationID=request.data.get('conversationID')
            )
            conversation.delete()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        
