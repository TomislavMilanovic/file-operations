from django.urls import path

from .views import search_files_view, download_files_view, move_file_view, api_docs_view

urlpatterns = [
    path('search-files/', search_files_view, name='search_files'),
    path('download-files/', download_files_view, name='download_files'),
    path('move-file/', move_file_view, name='move_file'),
    path('docs/', api_docs_view, name='api_docs'),
]
