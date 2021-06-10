from courses.models import Course, Your_Course
from django.db.models import Q


def get_courses(request, is_search, keyword=None):
    '''
    Get courses from database based on request type
    :param request: request from client
    :param is_search: (boolean) request is search query
    :param keyword: (if any) keyword in search query
    :return: dict 
    '''
    courses = {}
    favorite_id = []
    if request.user.is_authenticated:
        # if user signed in successfully, get all favorite course ids from database
        favorite_id = [
            c.course_id for c in Your_Course.objects.filter(user=request.user)]

    if keyword:
        if is_search:
            # Look up keyword in course name and course tags if user search for course
            look_up_courses = Course.objects.filter(
                Q(course_name__icontains=keyword) | Q(tags__icontains=keyword))
        else:
            # Look up keyword in course tags only, if user wants to show more courses with same tag
            look_up_courses = Course.objects.filter(id__in=favorite_id)
    else:
        # Get all courses in database to display on home page
        look_up_courses = Course.objects.all()

    # Mark favorite course if user signed in
    for c in look_up_courses:
        if c.id in favorite_id:
            courses[c] = True
        else:
            courses[c] = False
    return courses
