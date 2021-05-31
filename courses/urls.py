from django.urls import path
from django.urls import include
from .views import CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

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
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="courses/password_reset.html",
             email_template_name='courses/password_reset_email.html',
             success_url=reverse_lazy('courses:password_reset_done')),
         name="password_reset"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="courses/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="courses/password_reset_form.html",
             success_url=reverse_lazy('courses:password_reset_complete')),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="courses/password_reset_done.html"),
         name="password_reset_complete"),

]
