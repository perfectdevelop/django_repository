
from django.urls import path

from core.views import (index, register, login_view,
                        update_donator, delete_donator, logout_user, order_create,get_json)

urlpatterns = [
    path('', index, name="index"),
    path('register', register, name="index"),
    path('login', login_view, name="login"),
    path('logout', logout_user, name="logout"),
    path('update_donator/', update_donator, name='update_donator'),
    path('delete/<int:id>/', delete_donator, name='delete_donator'),
    path('order/<pat>/<don>/', order_create, name='orders'),
    path('graph', get_json, name="get_json")
]
