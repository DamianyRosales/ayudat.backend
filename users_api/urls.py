from django.urls import path, include
from users_api import views


app_name = 'users_api'


urlpatterns = [
    #Registration Urls
    path('admin/', views.admin_list),
    #path('professional/', views.professional_list),
    #path('professional/', views.professional_view.as_view()),
    path('professional/<int:pk>/', views.professional_view.as_view()),
    # path('mod/', ModRegistrationView.as_view(), name='register-mod'),
    # path('professional/', ProfessionalRegistrationView.as_view(), name='register-professional'),
    # path('patient/', PatientRegistrationView.as_view(), name='register-patient'),
    # #path('login/',Login.as_view(), name='login')
]