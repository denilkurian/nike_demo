from .views import RegistrationView,LoginView,logout_view
from django.urls import path

urlpatterns =[

    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

