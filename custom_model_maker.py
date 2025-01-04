import os

manager = """
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    \"""
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    \"""
    def create_user(self, email, password, **extra_fields):
        \"""
        Create and save a user with the given email and password.
        \"""
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        \"""
        Create and save a SuperUser with the given email and password.
        \"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
"""

forms = """
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
"""

model = "models.py"
models_code = """
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
"""
admin = 'admins.py'
admin_code = """
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_active", "date_joined")
    search_fields = ("email",)
    list_filter = ("is_active", "is_staff")
    ordering = ("email",)
"""

# Check if the file exists and overwrite it with new content
if os.path.exists(model):
    with open(model, "w") as file:
        file.write(models_code)
        # ======================
        with open("managers.py", "w") as file:
            file.write(manager)
        with open("forms.py", "w") as file:
            file.write(forms)

elif os.path.exists(admin):
    with open(admin, "w") as file:
        file.write(admin_code)
else:
    print(f"{model} does not exist.")



