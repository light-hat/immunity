import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя системы.
    """

    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self):
        return str(self.username)


class Application(models.Model):
    """
    Модель анализируемого приложения.
    """

    LANGUAGES = (("python", "Python"),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=255, choices=LANGUAGES)
    online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Агенты"
        verbose_name = "Агент"

    def __str__(self):
        return str(id)


class Context(models.Model):
    """
    Модель контекста.
    Данные об обработанном запросе инструментированным приложением.
    """

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    """
    Модель запроса.
    Содержит данные об обработанном запросе и является частью контекста.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    method = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    body = models.TextField()
    headers = models.TextField()
    user = models.CharField(max_length=255)
    get_params = models.TextField()
    post_params = models.TextField()
    cookies = models.TextField()
    files = models.TextField()
    meta = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ControlFlow(models.Model):
    """
    Модель потока управления.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)


class FunctionCall(models.Model):
    """
    Модель узла потока управления.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_flow = models.ForeignKey(ControlFlow, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    external_call = models.BooleanField()
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    args = models.TextField()


class CodeExecution(models.Model):
    """
    Модель обработки выполнения строки кода.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_flow = models.ForeignKey(ControlFlow, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    func_name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    args = models.TextField()
    code = models.TextField()


class ReturnFunction(models.Model):
    """
    Модель обработки возврата из функции.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_flow = models.ForeignKey(ControlFlow, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    func_name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    final_state = models.TextField()
    returned_value = models.TextField()


class Error(models.Model):
    """
    Модель возникшего исключения.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_flow = models.ForeignKey(ControlFlow, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    source_function = models.CharField(max_length=255)
    source_module = models.CharField(max_length=255)
    source_filename = models.CharField(max_length=255)
    source_line = models.CharField(max_length=255)
    exception_type = models.CharField(max_length=255)
    exception_message = models.TextField()


class Response(models.Model):
    """
    Модель ответа.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    status_code = models.CharField(max_length=255)
    headers = models.TextField()
    body = models.TextField()
    content_type = models.CharField(max_length=255)
    content_length = models.CharField(max_length=255)
    charset = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    reason_phrase = models.CharField(max_length=255)
    cookies = models.TextField()
    streaming = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
