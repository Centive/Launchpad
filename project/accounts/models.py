from secrets import token_urlsafe

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.querysets.user_profile import UserProfileQuerySet


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.id_external = token_urlsafe(16)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def user_exists(self, email):
        try:
            super().get_queryset().get(email=email)
            return True
        except ObjectDoesNotExist:
            return False

    def get_user_by_email(self, email):
        return super().get_queryset().get(email__exact=email)


class User(AbstractBaseUser, PermissionsMixin):
    # Columns
    #
    id_external = models.CharField(
        max_length=64
    )
    email = models.EmailField(
        unique=True,
        null=True
    )
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Configuration
    #
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class PresenceCountry(models.Model):
    # Columns
    #
    country_name = models.EmailField(
        unique=True
    )
    iso_2 = models.CharField(
        max_length=2
    )
    iso_3 = models.CharField(
        max_length=3
    )
    dialing_code = models.IntegerField()
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Configuration
    #
    def __str__(self):
        return '%s (+%s)' % (self.country_name, self.dialing_code)


class UserProfile(models.Model):
    # Columns
    #
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        'First name',
        max_length=255
    )
    last_name = models.CharField(
        'Last name',
        max_length=255
    )
    country = models.ForeignKey(
        PresenceCountry,
        on_delete=models.PROTECT
    )
    phone = models.IntegerField(
        'Phone number'
    )

    # Configuration
    #
    objects = UserProfileQuerySet.as_manager()

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.user_id)

    def get_full_phone_number(self):
        return '+%s%s' % (self.country.dialing_code, self.phone)
