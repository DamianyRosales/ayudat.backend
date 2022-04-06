from pyexpat import model
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from django.views.decorators.csrf import csrf_exempt
from users_api.serializers import (
    AdminSerializer, ProfessionalSerializer
    )
from . import models

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_auth.registration.views import RegisterView

from rest_framework.response import Response

import json
from urllib.parse import parse_qs

from rest_framework import status

# Create your views here.


@csrf_exempt
def admin_list(request):
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


class professional_view(APIView):
    
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk, format=None):
        professionals = models.Professional.objects.all()
        serializer = ProfessionalSerializer(professionals, many=True)
        return JsonResponse(serializer.data, safe=False)

    
    def put(self, request, pk, format=None):
        pass

    def post(self,request, pk):
        # data = JSONParser().parse(request.data)
        print('**********')
        print('**********')
        # print(request.data)
        print('**********')
        # print(request.data['document1'])
        request2={
            'document1':request.data.get('document1'),
            'document2':request.data.get('document2')
        }

        request.data.pop('document1')
        request.data.pop('document2')
        
        

        data = json.loads(json.dumps(request.data))
        

        # data = json.dumps(parse_qs(request.data))
        

        serializer = ProfessionalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            serializer2 = ProfessionalSerializer(data=request2)
            if serializer2.is_valid():
                serializer2.save()

            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    # def put(self,request, pk):
    #     try:
    #         professional = models.Professional.objects.get(pk=pk)
    #     except models.Professional.DoesNotExist:
    #         return HttpResponse(status=404)

    #     data = JSONParser().parse(request)
    #     serializer = ProfessionalSerializer(professional, data=data)

    #     if serializer.is_valid():

    #         serializer.save()

    #         if 'document1' not in request.data:
    #             raise ParseError("Missing document1")
    #         elif 'document2' not in request.data:
    #             raise ParseError("Missing document2")

    #         f = request.data['document1']
    #         f2 = request.data['document2']

    #         models.Professional.document1.save(f.name, f, save=True)
    #         models.Professional.document2.save(f2.name, f2, save=True)

    #         return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
    #         #return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)
    
    # def delete(self, request, pk):
    #     try:
    #         professional = models.Professional.objects.get(pk=pk)
    #     except models.Professional.DoesNotExist:
    #         return HttpResponse(status=404)
    #     professional.delete()
    
    

@csrf_exempt
def professional_list(request, pk):

    parser_class = (FileUploadParser,)

    try:
        professional = models.Professional.objects.get(pk=pk)
    except models.Professional.DoesNotExist:
        return HttpResponse(status=404)


    if request.method == 'GET':
        professionals = models.Professional.objects.all()
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
            if 'document1' not in request.data:
                raise ParseError("Missing document1")
            elif 'document2' not in request.data:
                raise ParseError("Missing document2")

            f = request.data['document1']
            f2 = request.data['document2']

            models.Professional.document1.save(f.name, f, save=True)
            models.Professional.document2.save(f2.name, f2, save=True)

            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
            #return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        professional.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#         if 'document1' not in request.data:
#             raise ParseError("Missing document1")
#         elif 'document2' not in request.data:
#             raise ParseError("Missing document2")

#         f = request.data['document1']
#         f2 = request.data['document2']

#         models.Professional.document1.save(f.name, f, save=True)
#         models.Professional.document2.save(f2.name, f2, save=True)

#         return Response(status=status.HTTP_201_CREATED)

# class MyUploadView(APIView):
#     parser_class = (FileUploadParser,)

#     def put(self, request, format=None):
#         if 'document1' not in request.data:
#             raise ParseError("Missing document1")
#         elif 'document2' not in request.data:
#             raise ParseError("Missing document2")

#         f = request.data['document1']
#         f2 = request.data['document2']

#         models.Professional.document1.save(f.name, f, save=True)
#         models.Professional.document2.save(f2.name, f2, save=True)

#         return Response(status=status.HTTP_201_CREATED)
    
#     def delete(self, request, format=None):
#         models.Professional.document1.delete(save=True)
#         return Response(status=status.HTTP_204_NO_CONTENT)