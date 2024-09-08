from django.urls import path
from django.http import HttpResponse


# added this avoid favico.ico warning
def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


urlpatterns = [
    path('favicon.ico', okay),
]
