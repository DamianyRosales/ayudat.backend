from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from users_api.serializers import (
    AdminSerializer, ModSerializer, 
    ProfessionalSerializer, PatientSerializer
    )

from . import models
# Create your views here.

@csrf_exempt
def admin_list(request, pk=None):

    try:
        admin = models.Admin.objects.get(pk=pk)
    except models.Admin.DoesNotExist:
        return HttpResponse(status=404)


    if request.method == 'GET':
        admins = models.Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AdminSerializer(admin, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        admin.delete()
        return HttpResponse(status=204)

@csrf_exempt
def professional_list(request, pk):

    try:
        professional = models.Professional.objects.get(pk=pk)
    except models.Professional.DoesNotExist:
        return HttpResponse(status=404)


    if request.method == 'GET':
        professionals = models.professional.objects.all()
        serializer = ProfessionalSerializer(professionals, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfessionalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProfessionalSerializer(professional, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        professional.delete()
        return HttpResponse(status=204)