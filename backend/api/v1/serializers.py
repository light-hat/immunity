"""
Определение сериализаторов для API-обработчиков.
"""

from api.models import (Folder, File)
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для файлов.
    """

    class Meta:
        model = File
        fields = '__all__'


class FolderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для директорий.
    """

    class Meta:
        model = Folder
        fields = '__all__'
