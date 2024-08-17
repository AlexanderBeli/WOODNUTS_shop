from django.urls import path

from .views import (
    ChangePasswordView,
    SignupPageView,
    UserPageDetailView,
    UserUpdateView,
)

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("info/<int:pk>/", UserPageDetailView.as_view(), name="userinfo"),
    path("info/<int:pk>/edit/", UserUpdateView.as_view(), name="userinfoedit"),
    path("info/<int:pk>/editpassword/", ChangePasswordView.as_view(), name="editpw"),
]
