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
    parser_classes = (parsers.FormParser)


class FileViewSet(viewsets.ModelViewSet):
    """
    DRF Viewset для файлов.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # authentication_classes = [TokenAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    def create(self, request, *args, **kwargs):
        """
        Переопределение метода create. Сохраняет загружаемый файл в загруженные.
        :param request: Объект запроса пользователя.
        :param args: Дополнительные позиционные аргументы.
        :param kwargs: Дополнительные именованные аргументы.
        :return: Объект API-ответа в формате JSON.
        """
        archive = request.FILES.get('archive')
        version = request.data.get('version')
        version_original = request.data.get('version_original')
        description = request.data.get('description')

        file_metadata = Firmware.objects.create(
            version=version,
            version_original=version_original,
            description=description
        )

        if isinstance(archive, UploadedFile):
            file_metadata.archive = archive
        else:
            raise serializers.ValidationError("Файл не был предоставлен.")

        file_metadata.save()

        return Response({
            'version': file_metadata.version,
            'version_original': file_metadata.version_original,
            'description': file_metadata.description,
        })
