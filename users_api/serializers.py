from rest_framework import serializers
from users_api.models import Admin, Professional, Patient, Mod

class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = '__all__'


class ModSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Professional
        fields = '__all__'


class ProfessionalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Professional
        fields = '__all__'


class PatientSerializer(serializers.Serializer):
    
    class Meta:
        model = Patient
        fields = '__all__'

