from django.db import models

from downtube.users.models import User


class Video(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    url = models.CharField(max_length=120, verbose_name="Youtube ссылка")
    title = models.TextField(verbose_name="Название")
    video = models.TextField(verbose_name="Видео")

    def save(self, *args, **kwargs):
        user_streams = Video.objects.filter(user=self.user)
        if not user_streams.exists():
            super().save(*args, **kwargs)
        if not user_streams.filter(url=self.url).exists():
            if user_streams.count() >= 10:
                delete_stream = user_streams.first()
                delete_stream.delete()
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
