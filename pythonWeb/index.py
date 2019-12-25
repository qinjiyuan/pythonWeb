from django.http.response import HttpResponse


def index(request):
    return HttpResponse(b'Hello World')
