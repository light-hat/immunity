"""
Описание модели базы данных.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

OBJECT_VISIBILITY = (
    ('public', 'Публичный доступ'),
    ('private', 'Приватный доступ'),
)


class User(AbstractUser):
    """
    Кастомная модель пользователя системы.
    """
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self):
        return str(self.username)


class Folder(models.Model):
    """
    Модель директории файлообменника.
    """
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    visible = models.CharField(
        "Видимость",
        max_length=10,
        choices=OBJECT_VISIBILITY,
        default="private"
    )

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Директории"
        verbose_name = "Директория"

    def __str__(self):
        return str(self.name)


class File(models.Model):
    """
    Модель загруженного пользователем файла.
    """

    FILE_STATES = (
        ('processing', 'В обработке'),
        ('ready', 'Готово'),
        ('error', 'Ошибка анализа'),
    )

    FILE_TYPES = (
        ('unknown', 'Неизвестно'),
        ('photo', 'Фотография'),
        ('video', 'Видеозапись'),
        ('audio', 'Аудиозапись'),
        ('document', 'Документ'),
        ('archive', 'Архив'),
        ('exe', 'Исполняемый файл'),
    )

    def path_to_directory(instance, filename):
        """
        Формирование файловой структуры.
        """
        return f"upload_files/{instance.owner.username}/{filename}"

    filename = models.CharField("Имя файла", default="unknown", max_length=500)
    extension = models.CharField("Расширение", default="unknown", max_length=15)
    folder = models.ForeignKey(
        Folder,
        null=True,
        blank=True,
        related_name='files',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        on_delete=models.CASCADE
    )
    url = models.FileField(
        "Файл",
        upload_to=path_to_directory
    )
    type = models.CharField(
        "Тип файла",
        max_length=10,
        choices=FILE_TYPES,
        default="unknown"
    )
    state = models.CharField(
        "Состояние",
        max_length=10,
        choices=FILE_STATES,
        default="processing"
    )
    visible = models.CharField(
        "Видимость",
        max_length=10,
        choices=OBJECT_VISIBILITY,
        default="private"
    )
    size = models.PositiveIntegerField("Размер файла", null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Файлы"
        verbose_name = "Файл"

    def __str__(self):
        return f"{self.filename}.{self.extension}"
