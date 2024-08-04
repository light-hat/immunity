"""
Определение вьюсетов для обработки REST API-запросов.
"""

from api.models import (Folder, File)
from api.v1.serializers import (FolderSerializer, FileSerializer)
from rest_framework import viewsets, parsers


class FolderViewSet(viewsets.ModelViewSet):
    """
    DRF Viewset для директорий.
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    # authentication_classes = [TokenAuthentication]
    parser_classes = (parsers.JSONParser, parsers.FormParser)


class FileViewSet(viewsets.ModelViewSet):
    """
    DRF Viewset для файлов.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # authentication_classes = [TokenAuthentication]
    parser_classes = (parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
