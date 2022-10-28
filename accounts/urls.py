from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path("register/", views.sign_up, name="sign_up"),
    path("login/", views.sign_in, name="sign_in"),
    path("logout/", views.logout_user, name="logout"),
]
