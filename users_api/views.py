from pyexpat import model
from webbrowser import get
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from django.views.decorators.csrf import csrf_exempt
from users_api.serializers import (
    AdminSerializer, ProfessionalSerializer, Professional2Serializer, PatientSerializer,ModSerializer
    )
from . import models

from rest_framework.views import APIView

import json
from rest_framework import status

from rest_framework import response

# Create your views here.


class admin_view(APIView):
    
    def get(self, request, format=None):

        admins = models.Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        
        return JsonResponse(serializer.data, safe=False)

    
    def put(self, request, pk=None):
        data = request.data
        data = json.loads(json.dumps(request.data))
        
        
        for e in models.Patient.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

        admin = models.Admin.objects.get(email=email)

        serializer = AdminSerializer(admin, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data)

    def delete(self, request, format=None):
        for e in models.Admin.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                admin = models.Admin.objects.get(email=email)
                admin.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    def post(self,request):

        data = json.loads(json.dumps(request.data))
        
        serializer = AdminSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()    

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class professional_view(APIView):
    
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, format=None):

        professionals = models.Professional.objects.all()
        serializer = ProfessionalSerializer(professionals, many=True)
        
        return JsonResponse(serializer.data, safe=False)

    
    def put(self, request, pk=None):
        data = request.data
        data = json.loads(json.dumps(request.data))
        
        
        for e in models.Professional.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

        professional = models.Professional.objects.get(email=email)

        serializer = ProfessionalSerializer(professional, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data)

    def delete(self, request, format=None):
        for e in models.Professional.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                professional = models.Professional.objects.get(email=email)
                professional.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    def post(self,request):

        request2 = {
            'document1':request.data.get('document1'),
            'document2':request.data.get('document2')
        }

        request.data.pop('document1')
        request.data.pop('document2')

        data = json.loads(json.dumps(request.data))
        
        serializer = ProfessionalSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()
            
            for e in models.Professional.objects.all():
                
                if e.email == request.data.get('email'):
                    pk = e.id
                    
            professional = models.Professional.objects.get(pk=pk)
            serializer2 = Professional2Serializer(professional, data=request2)
        
            if serializer2.is_valid():
                serializer2.save()
            

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class patient_view(APIView):
    
    def get(self, request, format=None):

        patients = models.Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        
        return JsonResponse(serializer.data, safe=False)

    
    def put(self, request, pk=None):
        data = request.data
        data = json.loads(json.dumps(request.data))
        
        
        for e in models.Patient.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

        patient = models.Patient.objects.get(email=email)

        serializer = PatientSerializer(patient, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data)

    def delete(self, request, format=None):
        for e in models.Patient.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                patient = models.Patient.objects.get(email=email)
                patient.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    def post(self,request):

        data = json.loads(json.dumps(request.data))
        
        serializer = PatientSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()    

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class mod_view(APIView):
    
    def get(self, request, format=None):

        patients = models.Mod.objects.all()
        serializer = ModSerializer(patients, many=True)
        
        return JsonResponse(serializer.data, safe=False)

    
    def put(self, request, pk=None):
        data = request.data
        data = json.loads(json.dumps(request.data))
        
        
        for e in models.Mod.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

        mod = models.Mod.objects.get(email=email)

        serializer = ModSerializer(mod, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data)

    def delete(self, request, format=None):
        for e in models.Mod.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                mod = models.Mod.objects.get(email=email)
                mod.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    def post(self,request):

        data = json.loads(json.dumps(request.data))
        
        serializer = ModSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()    

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


