from django.urls import path

from .views import HistoryStreamView, download_stream, upload_stream

app_name = "app"
urlpatterns = [
    path("", upload_stream, name="home"),
    path("history/<int:pk>/", HistoryStreamView.as_view(), name="history"),
    path("history/download/<path:link>/", download_stream, name="download"),
]
