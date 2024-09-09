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

