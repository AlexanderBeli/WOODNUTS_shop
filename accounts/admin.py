from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

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
    list_filter = ("is_active", "is_admin", "gender", "is_activated")
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")
    date_hierarchy = "date_joined"
    ordering = ["date_joined", "date_of_birth"]

    fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        (
            _("Personal info"),
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
        (
            _("Permissions"),
            {
                "fields": [
                    "groups",
                    "user_permissions",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        (
            _("Personal info"),
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
    ]


admin.site.register(CustomUser, CustomUserAdmin)
