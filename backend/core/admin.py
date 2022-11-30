from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Link, Order, OrderItem, Product, User, Profile


class SuperUser(UserAdmin):
    ordering = ["id"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "gender", "phone_number", "country", "city"]
    list_filter = ["gender", "country", "city"]
    list_display_links = ["id", "pkid"]

admin.site.register(User, SuperUser)
admin.site.register(Product)
admin.site.register(Link)
admin.site.register(Order)
admin.site.register(OrderItem)




admin.site.register(Profile, ProfileAdmin)