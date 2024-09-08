from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# added this to avoid favicon.ico warning
def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', okay),
    path('', include('myapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
