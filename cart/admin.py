from django.contrib import admin
from .models import Item, Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('price',)

admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)