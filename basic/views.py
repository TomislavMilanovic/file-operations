import os
import json
import glob
import zipfile

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def get_files(request):
    base_folder = settings.BASE_FILE_OPERATIONS_FOLDER
    wildcard = request.GET.get('wildcard', '')

    if wildcard:
        final_wildcard = "/**/" + wildcard
    else:
        final_wildcard = "/**/*"

    filepaths = glob.glob(base_folder + final_wildcard, recursive=True)

    return filepaths


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('OK')},
    manual_parameters=[
        openapi.Parameter(
            'wildcard',
            openapi.IN_QUERY,
            description='Wildcard pattern for file search',
            type=openapi.TYPE_STRING
        ),
    ]
)
@api_view(['GET'])
def search_files(request):
    base_folder = settings.BASE_FILE_OPERATIONS_FOLDER

    filepaths = get_files(request)
    filepaths = [os.path.relpath(filepath, base_folder)
                 for filepath in filepaths]
    response_data = {'filepaths': filepaths}

    return JsonResponse(response_data)


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('OK')},
    manual_parameters=[
        openapi.Parameter(
            'wildcard',
            openapi.IN_QUERY,
            description='Wildcard pattern for file search',
            type=openapi.TYPE_STRING
        ),
    ]
)
@api_view(['GET'])
def download_files(request):
    base_folder = settings.BASE_FILE_OPERATIONS_FOLDER

    filepaths = get_files(request)

    if len(filepaths) == 0:
        return JsonResponse({'message': 'No files to download'})

    response = HttpResponse(content_type='application/zip')
    zip_filename = 'downloaded_files.zip'
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
        zip_filename)

    with zipfile.ZipFile(response, 'w') as zip_file:
        for filepath in filepaths:
            rel_path = os.path.relpath(filepath, base_folder)
            zip_file.write(filepath, rel_path)

    return response


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'source_path': openapi.Schema(type=openapi.TYPE_STRING),
        'destination_path': openapi.Schema(type=openapi.TYPE_STRING),
    }
), responses={200: openapi.Response('OK')})
@api_view(['POST'])
def move_file(request):
    base_folder = settings.BASE_FILE_OPERATIONS_FOLDER

    request_body = json.loads(request.body)

    source_path_relative = request_body.get('source_path', '')
    destination_path_relative = request_body.get('destination_path', '')

    source_path = os.path.join(base_folder, source_path_relative)
    destination_path = os.path.join(base_folder, destination_path_relative)

    if not os.path.exists(source_path):
        return JsonResponse({'message': 'Source path does not exist'}, status=400)

    if os.path.isdir(destination_path):
        return JsonResponse({'message': 'Destination path should include a filename'}, status=400)

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    try:
        os.rename(source_path, destination_path)
        return JsonResponse({'message': 'File moved successfully'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


schema_view = get_schema_view(
    openapi.Info(
        title="File Operations API",
        default_version="v1",
        description="Simple API for operations with files",
        contact=openapi.Contact(email="tomislav.milanovic@outlook.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)


def api_docs_view(request):
    return schema_view.with_ui('swagger', cache_timeout=0)(request)
