from django.urls import path, include
from users_api import views

app_name = 'users_api'


urlpatterns = [
    #Registration Urls
    path('professional/', views.professional_view.as_view()),
    path('professional/accept/', views.accept_professional),
    path('patient/', views.patient_view.as_view()),
    path('mod/', views.mod_view.as_view()),
    path('admin/', views.admin_view.as_view()),
    # path('professional/<str:email>', views.professional_view.as_view()),
]