from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "is_superuser",
    ]
    fieldsets = (
        (None, {"fields": ["username", "email", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "phone_number",
                ]
            },
        ),
    )
    add_fieldsets = (
        (None, {"fields": ["username", "email", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "phone_number",
                ]
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
