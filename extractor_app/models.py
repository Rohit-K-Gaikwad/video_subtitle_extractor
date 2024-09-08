from django.db import models


class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    start_time = models.DurationField()
    end_time = models.DurationField()
    content = models.TextField()

    def __str__(self):
        return f"{self.video.file.name} - {self.language} [{self.start_time} - {self.end_time}]"

