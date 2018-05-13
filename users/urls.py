from django.urls import path
from users.views import index_view, images_view, signup, login, logout

urlpatterns = [
    path('images/index', index_view, name='index'),
    path('images', images_view, name='image_add'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
]
