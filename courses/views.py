from .models import Course, Your_Course
from courses.util import get_thumbnail_url
from courses.form import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json


def index(request):
    all_courses = {}

    if request.user.is_authenticated:
        favorite_id = [
            c.course_id for c in Your_Course.objects.filter(user=request.user)]

    for course in Course.objects.all():
        all_courses[course] = False
        if request.user.is_authenticated:
            if course.id in favorite_id:
                all_courses[course] = True

    context = {'courses': all_courses}
    return render(request, 'courses/courses.html', context)


def search_course(request):
    keyword = request.GET.get('key')
    if not keyword.split():
        all_courses = Course.objects.all()
        context = {'courses': all_courses}
        return render(request, 'courses/courses.html', context)

    courses = Course.objects.filter(
        Q(course_name__icontains=keyword) | Q(keywords__icontains=keyword))
    context = {'courses': courses, 'keyword': keyword}

    return render(request, 'courses/search.html', context)


def category(request, key):
    if key:
        courses = Course.objects.filter(keywords__icontains=key)
        context = {'courses': courses}
    else:
        all_courses = Course.objects.all()
        context = {'courses': all_courses}
    return render(request, 'courses/courses.html', context)


def toggle_favorite(request):
    data_from_post = json.load(request)['course_id']
    course_id = data_from_post.split('-')[-1]
    if Your_Course.objects.filter(user=request.user).filter(course_id=course_id):
        Your_Course.objects.filter(user=request.user).filter(
            course_id=course_id).delete()
    else:
        q = Your_Course(user=request.user, course_id=course_id)
        q.save()
    return JsonResponse({})


class CustomLoginView(LoginView):
    template_name = 'courses/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('courses:index')


class RegisterPage(FormView):
    template_name = 'courses/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('courses:index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('courses:index')
        return super(RegisterPage, self).get(*args, **kwargs)


@ login_required(login_url='courses:login')
def show_favorite(request):
    favorite_id = [
        c.course_id for c in Your_Course.objects.filter(user=request.user)]
    favorite_courses = Course.objects.filter(id__in=favorite_id)
    context = {'favorite_courses': favorite_courses}
    return render(request, 'courses/favorite.html', context)


def suggest_course(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        course_name = request.POST.get('course_name')
        course_url = request.POST.get('course_url')
        tags = request.POST.get('tags')
        description = request.POST.get('description')
        thumbnail_url = get_thumbnail_url(course_url)
        try:
            Course.objects.create(
                course_name=course_name, url=course_url, keywords=tags, description=description)
        except Exception as e:
            print(e)

    return render(request, 'courses/suggest_course.html')
