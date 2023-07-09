from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, LoginSerializer
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import RegistrationForm
from register.models import User

class RegistrationView(generics.CreateAPIView,TemplateView):
    permission_classes = [permissions.AllowAny]
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            serializer = RegistrationSerializer(data=form.cleaned_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    success_url = reverse_lazy('listshoes')


    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)

        refresh = RefreshToken.for_user(user)

        response_data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.id
        }

        # return Response(status=HTTP_200_OK)
        # return Response(response_data, status=status.HTTP_200_OK)
        return redirect(self.success_url)



from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('listshoes')










