from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from users_api.serializers import (
    AdminSerializer, ProfessionalSerializer, Professional2Serializer, PatientSerializer,ModSerializer
    )
from . import models
from rest_framework.views import APIView
import json
from rest_framework import status
from rest_framework import response

from rest_framework.authtoken.views import ObtainAuthToken

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework import parsers, renderers
from rest_framework.response import  Response
from users_api.serializers import AuthCustomTokenSerializer, TokenObtainPairSerializer
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import permissions

from .models import Professional, Admin, Mod, UserBase, Patient

from django.utils.module_loading import import_string

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES

# Create your views here.

from rest_framework import generics, status

class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None
    _serializer_class = ""

    www_authenticate_realm = "api"

    def get_serializer_class(self):
        """
        If serializer_class is set, use it directly. Otherwise get the class from settings.
        """

        if self.serializer_class:
            return self.serializer_class
        try:
            return import_string(self._serializer_class)
        except ImportError:
            msg = "Could not import serializer '%s'" % self._serializer_class
            raise ImportError(msg)

    def get_authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        uemail = 'email'
        userType=-1
        for e in Patient.objects.all():
            if e.email == email:
                userType = e.userType
                uemail = e.email

        for e in Admin.objects.all():
            if e.email == email:
                userType = e.userType
                uemail = e.email
        for e in Mod.objects.all():
            if e.email == email:
                userType = e.userType
                uemail = e.email
        for e in Professional.objects.all():
            if e.email == email:
                professional = Professional.objects.get(email=e.email)
                
                serializer2 = ProfessionalSerializer(professional)
                userType = e.userType
                uemail = e.email
                document1 = serializer2.data['document1']
                document2 = serializer2.data['document2']
                
                try:
                    serializer.is_valid(raise_exception=True)
                except TokenError as e:
                    raise InvalidToken(e.args[0])

                return JsonResponse(data={
                    'data':serializer.validated_data, 
                    'userType':userType,
                    'email':uemail, 
                    'document1':document1, 
                    'document2':document2
                    }, 
                    status=status.HTTP_200_OK)

        

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(data={'data':serializer.validated_data, 'userType':userType, 'email':uemail}, status=status.HTTP_200_OK)

class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# class ObtainAuthToken(APIView):
#     throttle_classes = ()
#     permission_classes = ()
#     parser_classes = (
#         parsers.FormParser,
#         parsers.MultiPartParser,
#         parsers.JSONParser,
#     )

#     renderer_classes = (renderers.JSONRenderer,)

#     def post(self, request):
#         serializer = AuthCustomTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         content = {
#             'token': token.key,
#         }

#         return Response(content)

# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         token, created = Token.objects.get_or_create(user=email)
#         return Response({
#             'token': token.key,
#             'user_id': email.pk,
#             'email': email.email
#         })
        

class admin_view_post(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

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

                    return JsonResponse(data=serializer.data)

    def post(self,request):

        data = json.loads(json.dumps(request.data))
        
        serializer = AdminSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()    
            self.put(request)

            return JsonResponse(data=serializer.data, status=201)

        return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class admin_view(APIView):
    

    def get(self, request=None, format=None):

        admins = models.Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        
        return JsonResponse(data=serializer.data, safe=False)

    
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

            return JsonResponse(data=serializer.data)

    def delete(self, request, format=None):
        for e in models.Admin.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                admin = models.Admin.objects.get(email=email)
                admin.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    # def post(self,request):

    #     data = json.loads(json.dumps(request.data))
        
    #     serializer = AdminSerializer(data=data)

    #     if serializer.is_valid():
            
    #         serializer.save()    
    #         self.put(request)

    #         return JsonResponse(data=serializer.data, status=201)

    #     return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class professional_view_post(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    parser_classes = (MultiPartParser, FormParser)


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

            return JsonResponse(data=serializer.data)

    def post(self,request):

        request2 = {
            'document1':request.data.get('document1'),
            'document2':request.data.get('document2')
        }
        
        request.data._mutable = True

        request.data.pop('document1')
        request.data.pop('document2')

        data = json.loads(json.dumps(request.data))

        serializer = ProfessionalSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()
            self.put(request)
            for e in models.Professional.objects.all():
                
                if e.email == request.data.get('email'):
                    pk = e.id
                    
            professional = models.Professional.objects.get(pk=pk)
            serializer2 = Professional2Serializer(professional, data=request2)
        
            if serializer2.is_valid():
                serializer2.save()
                self.put(request)
            

            return JsonResponse(data=serializer.data, status=201)

        return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class professional_view(APIView):
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    
    parser_classes = (MultiPartParser, FormParser)

    allowed_methods = ['get', 'post', 'put', 'delete', 'options']
    # def options(self, request, id):
    #     response = HttpResponse()
    #     response['allow'] = ','.join([self.allowed_methods])
    #     return response
        
    def get(self, request, *args, **kwargs):
        professionals = models.Professional.objects.all()
        serializer = ProfessionalSerializer(professionals, many=True)
        
        return JsonResponse(data=serializer.data, safe=False)

    
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

            return JsonResponse(data=serializer.data)

    def delete(self, request, format=None):
        for e in models.Professional.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                professional = models.Professional.objects.get(email=email)
                professional.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    # def post(self,request):

    #     request2 = {
    #         'document1':request.data.get('document1'),
    #         'document2':request.data.get('document2')
    #     }

    #     request.data.pop('document1')
    #     request.data.pop('document2')

    #     data = json.loads(json.dumps(request.data))

    #     serializer = ProfessionalSerializer(data=data)

    #     if serializer.is_valid():
            
    #         serializer.save()
    #         self.put(request)
    #         for e in models.Professional.objects.all():
                
    #             if e.email == request.data.get('email'):
    #                 pk = e.id
                    
    #         professional = models.Professional.objects.get(pk=pk)
    #         serializer2 = Professional2Serializer(professional, data=request2)
        
    #         if serializer2.is_valid():
    #             serializer2.save()
    #             self.put(request)
            

    #         return JsonResponse(data=serializer.data, status=201)

    #     return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def accept_professional(request):
    data = json.loads(json.dumps(request.data))
    try:
        models.Professional.objects.get(email=data.get('email'))

        professional = models.Professional.objects.get(email=data.get('email'))
        professional.is_accepted = True
        professional.save()

        return JsonResponse(data='Aceptado.',status=status.HTTP_200_OK, safe=False)
    
    except:
    
        return JsonResponse(data='No existe el usuario.',status=status.HTTP_404_NOT_FOUND, safe=False)

class patient_view_post(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def put(self, request, pk=None):
        data = json.loads(json.dumps(request.data))
        
        
        for e in models.Patient.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

        patient = models.Patient.objects.get(email=email)

        serializer = PatientSerializer(patient, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(data=serializer.data)

    def post(self,request):

        data = json.loads(json.dumps(request.data))
        
        serializer = PatientSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()    
            self.put(request)

            return JsonResponse(data=serializer.data, status=201)

        return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class patient_view(APIView):
    
    def get(self, request=None, format=None):

        patients = models.Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        
        return JsonResponse(serializer.data, safe=False)

    
    def put(self, request, pk=None):
        data = json.loads(json.dumps(request.data))
        
        
        for e in models.Patient.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

        patient = models.Patient.objects.get(email=email)

        serializer = PatientSerializer(patient, data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(data=serializer.data)

    def delete(self, request, format=None):
        for e in models.Patient.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                patient = models.Patient.objects.get(email=email)
                patient.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    # def post(self,request):

    #     data = json.loads(json.dumps(request.data))
        
    #     serializer = PatientSerializer(data=data)

    #     if serializer.is_valid():
            
    #         serializer.save()    
    #         self.put(request)

    #         return JsonResponse(data=serializer.data, status=201)

    #     return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class mod_view_post(APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

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

            return JsonResponse(data=serializer.data)
    def post(self,request):

        data = json.loads(json.dumps(request.data))
        
        serializer = ModSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()    
            self.put(request)

            return JsonResponse(data=serializer.data, status=201)

        return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class mod_view(APIView):
    
    def get(self, request=None, format=None):

        patients = models.Mod.objects.all()
        serializer = ModSerializer(patients, many=True)
        
        return JsonResponse(data=serializer.data, safe=False)

    
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

            return JsonResponse(data=serializer.data)

    def delete(self, request, format=None):
        for e in models.Mod.objects.all():
            if e.email == request.data.get('email'):
                email = e.email

                mod = models.Mod.objects.get(email=email)
                mod.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        

    # def post(self,request):

    #     data = json.loads(json.dumps(request.data))
        
    #     serializer = ModSerializer(data=data)

    #     if serializer.is_valid():
            
    #         serializer.save()    
    #         self.put(request)

    #         return JsonResponse(data=serializer.data, status=201)

    #     return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


