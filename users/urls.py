from django.urls import path
from .views import RegisterView, LoginView, UserView, RefreshTokenView, AirportcreateView, AirportsView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('access-token',RefreshTokenView.as_view()),
    path('add/airport',AirportcreateView.as_view()),
    path('get/airport',AirportsView.as_view())
]
