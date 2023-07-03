from django.urls import path

from .views import search_files, download_files, move_file, api_docs_view

urlpatterns = [
    path('search-files/', search_files, name='search_files'),
    path('download-files/', download_files, name='download_files'),
    path('move-file/', move_file, name='move_file'),
    path('docs/', api_docs_view, name='api_docs'),
]
