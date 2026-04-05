from django.contrib import admin
from .models import Category, Event, TicketListing, Order, Payment, Message, UserProfile, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'time', 'price', 'is_featured')
    list_filter = ('category', 'date', 'is_featured')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'

@admin.register(TicketListing)
class TicketListingAdmin(admin.ModelAdmin):
    list_display = ('seller', 'event', 'ticket_type', 'quantity', 'price_per_ticket', 'is_active')
    list_filter = ('is_active', 'event')
    search_fields = ('seller__username', 'event__title')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'listing', 'tickets_bought', 'total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('buyer__username', 'listing__event__title')
    readonly_fields = ('order_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment_status', 'razorpay_order_id', 'created_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('user__username', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'listing', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')

admin.site.register(UserProfile)
admin.site.register(Review)
