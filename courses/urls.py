from django.urls import path
from django.urls import include
from .views import CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_course, name='search_course'),
    path('category/<str:key>', views.category, name='category'),
    path('toggle_favorite', views.toggle_favorite, name='toggle_favorite'),
    path('favorite', views.show_favorite, name='favorite'),
    path('suggest_course', views.suggest_course, name='suggest_course'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='courses:login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
]
