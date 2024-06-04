from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from dj.choices import Choices
from dj.choices.fields import ChoiceField


class Gender(Choices):
    _ = Choices.Choice

    female = _("female")
    male = _("male")
    unspecified = _("unspecified")

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name=_('first name'))
    last_name = models.CharField(max_length=100, verbose_name=_('last name'))
    username = models.CharField(max_length=100, verbose_name=_('username'), unique=True)
    date_joined = models.DateField(auto_now_add=True)          #автоматически
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('date of birth'))    #не обязательно к заполненю
    gender = ChoiceField(choices=Gender, default=Gender.unspecified, verbose_name=_('gender'))
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name=_('passed activation?'))
    send_messages = models.BooleanField(default=True, verbose_name=_('send significations about new comments'))
    phone_number = PhoneNumberField(verbose_name=_('phone number'))
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("users")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username