from rest_framework import serializers
from users_api.models import Admin, Professional, Patient, Mod

# Serializers define the API representation.


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = '__all__'


class ModSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mod
        fields = '__all__'


# class DocumentSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Document
#         fields = '__all__'


class ProfessionalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Professional
        fields = '__all__'

class Professional2Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Professional
        fields = ['document1','document2']


class PatientSerializer(serializers.Serializer):
    
    class Meta:
        model = Patient
        fields = '__all__'

