from django.urls import path, include
from users_api import views

app_name = 'users_api'


urlpatterns = [
    #Registration Urls
    path('professional/', views.professional_view.as_view()),
    path('professional/accept/', views.accept_professional),
    path('professional/create/', views.professional_view_post.as_view()),

    path('patient/', views.patient_view.as_view()),
    path('patient/create/', views.patient_view_post.as_view()),
    
    path('mod/', views.mod_view.as_view()),
    path('mod/create/', views.mod_view_post.as_view()),
    
    path('admin/', views.admin_view.as_view()),
    path('admin/create/', views.admin_view_post.as_view()),
    # path('professional/<str:email>', views.professional_view.as_view()),
]