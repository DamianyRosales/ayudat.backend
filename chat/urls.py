from django.urls import path
from chat import views

urlpatterns = [
    # path('<str:room_name>/', views.lobby)
    path('conversation/', views.conversation_view.as_view()),
]