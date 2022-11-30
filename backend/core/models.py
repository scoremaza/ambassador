from datetime import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TimeStampedUUIDModel
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, username, last_name, first_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_ambassador = False
        user.username = username
        user.last_name = last_name
        user.first_name = first_name
        user.deleted_at = None
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, last_name, first_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = True
        user.is_ambassador = True
        user.is_staff = True
        user.deleted_at = None
        user.username = username
        user.last_name = last_name
        user.first_name = first_name
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)



class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_ambassador = models.BooleanField(default=False)
    deleted_at  = models.DateTimeField(null=True, default=None)
    username = models.CharField(
        verbose_name=_("username"), db_index=True, max_length=255, unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    objects = UserManager()

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def revenue(self):
        orders = Order.objects.filter(user_id=self.pk, complete=True)
        return sum(o.ambassador_revenue for o in orders)
    
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
    
    def hard_delete(self):
        self.delete()



class Product(TimeStampedUUIDModel):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True)
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Link(TimeStampedUUIDModel):
    code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    


class Order(TimeStampedUUIDModel):
    transaction_id = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255)
    ambassador_email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    complete = models.BooleanField(default=False)
    

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def ambassador_revenue(self):
        items = OrderItem.objects.filter(order_id=self.pk)
        return sum(i.ambassador_revenue for i in items)

    @property
    def admin_revenue(self):
        items = OrderItem.objects.filter(order_id=self.pk)
        return sum(i.admin_revenue for i in items)


class OrderItem(TimeStampedUUIDModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product_title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    admin_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    ambassador_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    
class Profile(TimeStampedUUIDModel):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        
        
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), max_length=30, default="+250784123456"
    )
    about_me = models.TextField(
        verbose_name=_("about me"),
        default="say something about yourself",
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.MALE,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("country"), default="US", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("city"),
        max_length=180,
        default="Orlando",
        blank=False,
        null=False,
    )
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default="/profile_default.png"
    )
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    