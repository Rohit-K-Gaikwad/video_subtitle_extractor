# Built-in module imports
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.db import DatabaseError, IntegrityError
from django.conf import settings

# User-defined modules imports
from extractor_app.models import Video, Subtitle
from extractor_app.tasks import extract_subtitles, parse_and_save_subtitles


def video_list(request):
    """ Function to get the video as list"""
    try:
        if request.method == 'POST' and request.FILES['file']:
            video_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(video_file.name, video_file)
            video = Video.objects.create(file=filename)
            # Trigger background task for subtitle extraction
            extract_subtitles.delay(video.id)
            return redirect('video_list')
    except Exception as e:
        return HttpResponse(f"An error occurred while uploading the video: {str(e)}", status=500)

    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


def video_detail(request, video_id):
    try:
        video = get_object_or_404(Video, id=video_id)
        subtitles = Subtitle.objects.filter(video=video)
        return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles})
    except Video.DoesNotExist:
        return HttpResponse("Video not found", status=404)
    except DatabaseError as e:
        return HttpResponse(f"Database error: {str(e)}", status=500)


def search_subtitle(request, video_id):
    try:
        video = get_object_or_404(Video, id=video_id)
        query = request.GET.get('q', '')
        if query:
            subtitles = Subtitle.objects.filter(video=video, content__icontains=query)
            return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles, 'query': query})
        else:
            return redirect('video_detail', video_id=video_id)
    except Subtitle.DoesNotExist:
        return HttpResponse("Subtitles not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

