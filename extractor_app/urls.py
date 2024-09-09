from django.urls import path
from django.http import HttpResponse
from extractor_app import views


# added this avoid favico.ico warning
def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


urlpatterns = [
    path('favicon.ico', okay),
    path('', views.video_list, name='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/search/', views.search_subtitle, name='search_subtitle'),
]

