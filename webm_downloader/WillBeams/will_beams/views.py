from django.http import HttpResponse


def index(request):
    return HttpResponse('All set up {{MEDIA_URL}}')
