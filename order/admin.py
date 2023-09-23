from django.contrib import admin
from .models import Order, OrderItem, PromoCode

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'address', 'phone', 'created_at','status')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'address', 'phone')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

admin.site.register(PromoCode)