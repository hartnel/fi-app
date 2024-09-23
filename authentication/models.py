from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from authentication.constants import AdditionalPhoneNumberCts, RegexCts
from django.utils.timezone import now

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


# Create your models here.
phone_validator = RegexValidator(
    regex=RegexCts.PHONE_REGEX, message="Invalid phone number"
)



class CustomUserManager(BaseUserManager):

    # with phone number
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        phone_number = self.normalize_email(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)
    

class NonDeletedManager(CustomUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    # extra_field = models.CharField(blank=True, max_length=120)
    phone_number = models.CharField(
        blank=False,
        unique=True,
        null=False,
        max_length=120,
        validators=[phone_validator],
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        null=True,
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    
    phone_is_verified = models.BooleanField(default=False)

    # if emails is verified
    email_is_verified = models.BooleanField(default=False)

    # the deleted attribute
    is_deleted = models.BooleanField(default=False)

    objects = NonDeletedManager()

    all_objects = CustomUserManager()
    
    location = models.ForeignKey("common.Location", on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.phone_number})"
    
    
class AdditionalPhoneNumber(models.Model):
    phone_number = models.CharField(
        blank=False,
        unique=False,
        null=False,
        max_length=120,
        validators=[phone_validator],
    )
    
    type = models.CharField(max_length=120, blank=False, null=False, choices=AdditionalPhoneNumberCts.PHONE_NUMBER_TYPE_CHOICES, default=AdditionalPhoneNumberCts.NORMAL)
    
    is_verified = models.BooleanField(default=False)
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="additional_phone_numbers")