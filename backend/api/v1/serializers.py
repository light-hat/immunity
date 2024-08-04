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


class FileCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания файлов.
    """

    class Meta:
        model = File
        fields = [
            "url",
            "folder",
            "visible",
        ]


class FileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения файлов.
    """

    class Meta:
        model = File
        fields = [
            "filename",
            "visible",
        ]


class FolderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для директорий.
    """

    class Meta:
        model = Folder
        fields = '__all__'


class FolderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания директорий.
    """

    class Meta:
        model = Folder
        fields = [
            "name",
            "visible",
            "parent",
        ]


class FolderUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения директорий.
    """

    class Meta:
        model = Folder
        fields = [
            "name",
            "visible",
        ]
