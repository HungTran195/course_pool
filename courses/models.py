from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    url = models.URLField()
    thumbnail_url = models.URLField()
    description = models.TextField()
    tags = models.CharField(max_length=250)

    def __str__(self):
        return self.course_name

    def get_tags(self):
        tags = self.tags.split(',')
        return tags


class Your_Course(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    course_id = models.IntegerField()

    def __str__(self):
        return str(self.user) + ' - ' + str(self.course_id)


class Suggest_Course(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    course_name = models.CharField(max_length=250)
    course_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.course_name
