import json

from django.shortcuts import redirect, render

from .models import Course


def search(request):
    '''Works as a "buffer" for when we are obtaining data'''
    if request.method == 'GET':
        search = request.GET.get('find')
        # print('search', search)
        return redirect('coursetracker:course', pk=search)


def course(request, pk):
    '''Finds the Course object from the search term 'pk', returning that course's page if it exists.

    Inputs:
        - pk (str): search term, raw course name; must be in the format '<subject> <number><detail>', case insensitive
            - Not all course names have details
            - Examples: MATH 100, APSC 496D
    '''
    course_name = pk.upper()
    print(f"*Searching database for {course_name}")

    try:
        c = Course.objects.get(course_name__exact=course_name)
        print(f"*{course_name} found in database")
    except Course.DoesNotExist:
        print(f"*Course {course_name} does not exist")
        return render(request, 'coursetracker/404.html')

    sections_teaching_team = json.loads(c.sections_teaching_team)
    professor_ratings = json.loads(c.professor_ratings)
    preq_tree = json.loads(c.prerequisite_tree)

    return render(request, 'coursetracker/course.html', {'course': c, 'preq': preq_tree,
                                                         'sections_teaching_team': sections_teaching_team,
                                                         'professor_ratings': professor_ratings})
