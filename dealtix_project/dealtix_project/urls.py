from django.contrib import admin
from django.urls import path
from users.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view),
]