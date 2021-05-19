from .models import Course
from courses.util import get_thumbnail_url
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def index(request):
    all_courses = Course.objects.all()

    context = {'courses': all_courses}
    return render(request, 'courses/courses.html', context)


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


@login_required(login_url='courses:login')
def show_favorite(request):
    context = {'favorite_courses': 1}
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
