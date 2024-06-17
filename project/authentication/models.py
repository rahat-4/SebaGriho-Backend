from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

# from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField

from phonenumber_field.modelfields import PhoneNumberField

from .choices import BloodGroups, UserGender, UserStatus
from .managers import UserManager
from .utils import get_user_media_path_prefix, get_user_slug

from common.models import BaseModelWithUid


class User(AbstractBaseUser, BaseModelWithUid, PermissionsMixin):
    slug = AutoSlugField(populate_from=get_user_slug, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    phone = PhoneNumberField(blank=True)
    secondary_phone = PhoneNumberField(blank=True)
    secondary_email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    nid = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(
        "Avatar",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
        default=UserGender.MALE,
    )
    blood_group = models.CharField(
        max_length=5,
        blank=True,
        choices=BloodGroups.choices,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)
