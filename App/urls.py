from django.urls import path
from . import views

urlpatterns = [
    path("", views.List.as_view(), name="list"),
    path("create/", views.Create.as_view(), name="create"),
    path("update/<str:pk>", views.Update.as_view(), name="update"),
    path("detail/<str:pk>/", views.Detail.as_view(), name="detail"),
    path("delete/<str:pk>/", views.Delete.as_view(), name="delete"),
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
