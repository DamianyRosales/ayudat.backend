from rest_framework import serializers
from chat.models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     user = Admin.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )
    #     return user

    class Meta:
        model = Conversation
        fields = '__all__'
        
    # def update(self, instance, validated_data):
    #     if 'password' in validated_data:
    #         password = validated_data.pop('password')
    #         instance.set_password(password)
    #     return super().update(instance,validated_data)