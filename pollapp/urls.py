from django.urls import path
from .views import Home_View, Create_View, LoginView, Profile, SignupView, signout

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("home/", Home_View, name="home"),
    path("create/", Create_View, name="create"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", Profile, name="login"),
    path("logout/", signout, name="logout"),
]
