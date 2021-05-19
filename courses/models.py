from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    url = models.URLField()
    thumbnail_url = models.URLField()
    description = models.TextField()
    keywords = models.CharField(max_length=250)

    def __str__(self):
        return self.course_name

    def get_keywords(self):
        keywords = self.keywords.split(',')
        return keywords
