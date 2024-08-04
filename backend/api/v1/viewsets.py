"""
Определение вьюсетов для обработки REST API-запросов.
"""

from api.models import (Folder, File)
from api.v1.serializers import (
    FolderSerializer,
    FolderCreateSerializer,
    FolderUpdateSerializer,
    FileSerializer,
    FileCreateSerializer,
    FileUpdateSerializer
)
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, parsers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class FolderViewSet(viewsets.ModelViewSet):
    """
    DRF Viewset для директорий.
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @swagger_auto_schema(request_body=FolderUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        serializer = FolderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=FolderCreateSerializer)
    def create(self, request, *args, **kwargs):
        serializer = FolderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = request.data.get('name')
        parent = request.data.get('parent')
        visible = request.data.get('visible')

        folder_metadata = Folder.objects.create(
            name=name,
            visible=visible,
            parent=parent,
            owner=request.user,
        )

        folder_metadata.save()

        return Response({
            'id': folder_metadata.id,
            'name': folder_metadata.name,
            'visible': folder_metadata.visible,
            'parent': folder_metadata.parent,
        })


class FileViewSet(viewsets.ModelViewSet):
    """
    DRF Viewset для файлов.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @swagger_auto_schema(request_body=FileUpdateSerializer)
    def update(self, request, *args, **kwargs):
        serializer = FileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=FileUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        serializer = FileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=FileCreateSerializer)
    def create(self, request, *args, **kwargs):
        """
        Переопределение метода create. Сохраняет загружаемый файл в загруженные.
        """
        serializer = FileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = request.FILES.get('url')
        folder = request.data.get('folder')
        visible = request.data.get('visible')
        folder_instance = get_object_or_404(Folder, id=folder)

        file_metadata = File.objects.create(
            folder=folder_instance,
            visible=visible,
            owner=request.user,
        )

        if isinstance(url, UploadedFile):
            file_metadata.url = url
        else:
            raise serializers.ValidationError("Файл не был предоставлен.")

        file_metadata.save()

        return Response({
            'id': file_metadata.id,
            'folder': folder_instance.id,
            'visible': file_metadata.visible,
            'owner': file_metadata.owner.id,
        })
