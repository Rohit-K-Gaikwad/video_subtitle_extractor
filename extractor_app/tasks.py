import subprocess
import re,os
from celery import shared_task
from extractor_app.models import Video, Subtitle
from datetime import timedelta
from django.conf import settings
from django.db import IntegrityError, DatabaseError


@shared_task
def extract_subtitles(video_id):
    try:
        video = Video.objects.get(id=video_id)
        video_path = video.file.path

        # Languages to extract subtitles for (example: 'en' and 'es')
        languages = ['en', 'es']

        for language in languages:
            output_path_srt = f"{video_path}_{language}.srt"

            # Use ccextractor to extract subtitles for the given language
            subprocess.run(['ccextractor', video_path, '-o', output_path_srt])

            # Parse and save the subtitles
            with open(output_path_srt, 'r') as srt_file:
                srt_content = srt_file.read()

            parse_and_save_subtitles(srt_content, video, language)

        video.processed = True
        video.save()

    except Video.DoesNotExist:
        print(f"Video with id {video_id} does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video with ccextractor: {str(e)}")
    except Exception as e:
        print(f"An error occurred while extracting subtitles: {str(e)}")


def parse_and_save_subtitles(srt_content, video, language):
    """
    Parse the SRT file content and save subtitles in the database.
    """
    try:
        srt_blocks = re.split(r'\n\n', srt_content.strip())
        for block in srt_blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                times = lines[1].split(' --> ')
                start_time = parse_time(times[0])
                end_time = parse_time(times[1])
                content = ' '.join(lines[2:])
                Subtitle.objects.create(video=video, language=language, start_time=start_time, end_time=end_time, content=content)

    except IntegrityError as e:
        print(f"Database error when saving subtitles: {str(e)}")
    except Exception as e:
        print(f"Error parsing subtitles: {str(e)}")


def parse_time(time_str):
    """
    Convert SRT timestamp to timedelta.
    """
    try:
        hours, minutes, seconds = time_str[:8].split(':')
        milliseconds = time_str[9:]
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
    except ValueError as e:
        print(f"Error parsing time from SRT: {str(e)}")
        return timedelta(0)
