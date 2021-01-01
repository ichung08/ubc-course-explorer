import json

from django.shortcuts import redirect, render

from .models import Course

from .scrapers import ubcexplorer as ex, ubcgrades as gr

path_to_rmp_data = 'coursetracker/scrapers/rmp_ubc_profs_list.txt'

# search works as a "buffer" for when we are obtaining data
def search(request):
    if request.method == 'GET':
        search = request.GET.get('find')
        #print('search', search)
        return redirect('coursetracker:course', pk=search)

def course(request, pk):
        c = None
        try:
            # case insensitive search
            c = Course.objects.get(course_name__iexact=pk)
            #print("getting course")
        except Course.DoesNotExist:
            subAndCourse = pk.split(' ')
            if len(subAndCourse) == 2:
                subject = subAndCourse[0].upper()
                course = subAndCourse[1]
            else:
                subject = pk[0:-3].upper()
                course = pk[-3:]

            if not gr.subject_is_valid(subject) or not gr.course_is_valid(subject, course):
                return render(request, 'coursetracker/404.html')

            # TODO: decide whether to get term grade statistics (for high, low, pass, fail, etc.)
            stats = gr.course_statistics(subject, course)
            avg = stats['average']
            avg5 = stats['average_past_5_yrs']
            stdev = stats['stdev']

            distributions = gr.distributions(subject, course)  # need to process this, turn into graph
            
            profsList = gr.teaching_team(subject, course)
            
            ubcProfs = []
            try:
                with open(path_to_rmp_data) as json_file:
                    ubcProfs = json.load(json_file)
            except OSError:
                return render(request, 'coursetracker/404.html')
            
            profs = {}
            for prof in profsList:
                for profInfo in ubcProfs:
                    if prof == profInfo['tFname'] + ' ' + profInfo['tLname']:
                        profs[prof] = [profInfo['overall_rating'], profInfo['tNumRatings']]

            exp = ex.course_info_with_prereq_tree(subject, course)
            preq = exp['preq']  # need to process this, turn into tree
            creq = exp['creq']
            depn = exp['depn']
            name = exp['name']
            cred = exp['cred']
            desc = exp['desc']
            prer = "n/a" if 'prer' not in exp else exp['prer']
            crer = "n/a" if 'crer' not in exp else exp['crer']
            link = exp['link']

            c = Course(course_name=pk, average=avg, five_year_average=avg5, standard_deviation=stdev,
                       distributions=distributions, professors=profs, prerequisites=preq, corequisites=creq,
                       dependencies=depn, name=name, number_of_credits=cred, course_description=desc,
                       prerequistes_description=prer, corequisites_description=crer, link=link)
            c.save()
            #print("creating new course")

        return render(request, 'coursetracker/course.html', {'course': c})
