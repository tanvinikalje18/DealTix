from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/checkout/<int:listing_id>/', views.checkout, name='checkout'),
    path('events/buy/<int:listing_id>/', views.buy_ticket, name='buy_ticket'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('sell/', views.sell_ticket, name='sell_ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rate/<int:order_id>/', views.rate_seller, name='rate_seller'),
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<int:listing_id>/<int:buyer_id>/', views.chat_view, name='chat_view'),
]
