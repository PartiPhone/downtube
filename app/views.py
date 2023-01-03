import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic.list import ListView

from app.models import Video

from .forms import GuestDownloadForm, UserDownloadForm
from .utils import download_youtube_stream


def upload_stream(request):

    actual_form = GuestDownloadForm
    context = {
        "form": actual_form,
    }

    if request.method == "POST":
        actual_form = GuestDownloadForm(request.POST)
        if actual_form.is_valid():
            url = actual_form.cleaned_data["url"]
            stream_url = download_youtube_stream(url)
            if stream_url is None:
                actual_form = GuestDownloadForm()
                messages.add_message(request, messages.ERROR, "Видео недоступно")
            else:
                if request.user.is_authenticated:
                    user_form = UserDownloadForm(request.POST)
                    if user_form.is_valid():
                        uf = user_form.save(commit=False)
                        uf.title = os.path.split(stream_url)[1]
                        uf.user = request.user
                        uf.video = stream_url
                        # user_form.title = os.path.split(stream_url)[1]
                        # user_form.video = stream_url
                        # user_form.save()
                        uf.save()
                    else:
                        messages.add_message(request, messages.WARNING, "Ошибка")
                f = open(stream_url, "rb")
                return FileResponse(f, as_attachment=True)
        else:
            actual_form = GuestDownloadForm()
            messages.add_message(request, messages.WARNING, "Неверные данные")
    return render(request, "app/home.html", context)


@login_required
def download_stream(request, link):
    f = open(link, "rb")
    return FileResponse(f, as_attachment=True)


class HistoryStreamView(LoginRequiredMixin, ListView):
    model = Video
    template_name = "app/history.html"

    def get_queryset(self):
        return Video.objects.filter(user__pk=self.kwargs["pk"])[:10]
