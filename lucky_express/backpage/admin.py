from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User as Aduser
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.

mlssz_admin = admin.site # MlsszAdminSite("mlssz_admin")
mlssz_admin.site_header = "MLSSZ后台管理"
mlssz_admin.site_title = "MLSSZ"

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
    list_display = ("account", "realname", "ci", "picture_info")

    def account(self, obj):
        return obj.id.account

    def picture_info(self, instance):
        """construct a link to picture page."""
        return format_html(
            "<span><a href=\"/lessee/{}/pictures/?back=/admin/backpage/lessee/\">审查</a></span>",
            instance.id.id
        )

    picture_info.short_description = "图片信息"

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
