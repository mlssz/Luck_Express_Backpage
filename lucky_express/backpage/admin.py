from django.contrib import admin

from .models import *

# Register your models here.

class MlsszAdminSite(admin.AdminSite):
    """Special title and header of AdminSite"""
    site_header = "MLSSZ后台管理"
    site_title = "MLSSZ"

mlssz_admin = MlsszAdminSite("mlssz_admin")

@admin.register(User, site=mlssz_admin)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "name", "user_type")

@admin.register(Rental, site=mlssz_admin)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("account", "name", "score")

    def account(self, obj):
        return obj.id.account

    def name(self, obj):
        return obj.id.name


@admin.register(Lessee, site=mlssz_admin)
class LesseeAdmin(admin.ModelAdmin):
    list_display = ("account", "realname", "ci")

    def account(self, obj):
        return obj.id.account

@admin.register(Orders, site=mlssz_admin)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "rental", "lessee", "status")

@admin.register(Line, site=mlssz_admin)
class LineAdmin(admin.ModelAdmin):
    list_display = ("id", "rental", "lessee")

@admin.register(Truck, site=mlssz_admin)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("no", "lessee", "car_type")

@admin.register(Advertisement, site=mlssz_admin)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("info", "fee", "time")

@admin.register(Service, site=mlssz_admin)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("offer", "customer", "time")
