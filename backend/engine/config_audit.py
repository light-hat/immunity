"""
Модуль анализа конфигурации.
"""


class ConfigAuditStrategy:
    """Базовый класс стратегии аудита конфигурации."""

    def __init__(self, config):
        self.config = config
        self.issues = []

    def check(self, key, expected_value, message, check_type="equal"):
        """Базовая проверка конфигурации."""

        actual_value = self.config.get(key)

        if check_type == "equal" and actual_value != expected_value:
            self.issues.append({
                "key": key,
                "actual_value": actual_value,
                "message": message
            })
        elif check_type == "not_equal" and actual_value == expected_value:
            self.issues.append({
                "key": key,
                "actual_value": actual_value,
                "message": message
            })
        elif check_type == "exists" and actual_value is None:
            self.issues.append({
                "key": key,
                "actual_value": "None",
                "message": message
            })
        elif check_type == "in" and actual_value not in expected_value:
            self.issues.append({
                "key": key,
                "actual_value": actual_value,
                "message": message
            })
        elif check_type == "not_in" and actual_value in expected_value:
            self.issues.append({
                "key": key,
                "actual_value": actual_value,
                "message": message
            })

    def run_audit(self):
        """Метод для реализации конкретной стратегии."""
        raise NotImplementedError("Метод run_audit() должен быть реализован в подклассе.")


class DjangoConfigAudit(ConfigAuditStrategy):
    """Стратегия аудита для Django."""

    def run_audit(self):
        # Отладка
        self.check('DEBUG', "False", 'DEBUG должен быть отключен в продакшене.')

        # Безопасность
        self.check('SECRET_KEY', 'None', 'SECRET_KEY должен быть установлен и не быть значением по умолчанию.', check_type="not_equal")
        self.check('ALLOWED_HOSTS', '[\'*\']', 'ALLOWED_HOSTS не должен содержать "*".')
        self.check('SECURE_SSL_REDIRECT', 'True', 'SECURE_SSL_REDIRECT должен быть включен для перенаправления HTTP на HTTPS.')
        self.check('CSRF_COOKIE_SECURE', 'True', 'CSRF_COOKIE_SECURE должен быть включен для использования только с HTTPS.')
        self.check('SESSION_COOKIE_SECURE', 'True', 'SESSION_COOKIE_SECURE должен быть включен для защиты cookie через HTTPS.')
        self.check('SECURE_HSTS_SECONDS', '0', 'SECURE_HSTS_SECONDS должен быть больше нуля для активации HSTS.', check_type="not_equal")
        self.check('SECURE_BROWSER_XSS_FILTER', 'True', 'SECURE_BROWSER_XSS_FILTER должен быть включен для защиты от XSS.')
        self.check('SECURE_CONTENT_TYPE_NOSNIFF', 'True', 'SECURE_CONTENT_TYPE_NOSNIFF должен быть включен для предотвращения MIME-атаки.')
        self.check('X_FRAME_OPTIONS', 'DENY', 'X_FRAME_OPTIONS должен быть установлен в "DENY" для предотвращения кликовых атак.')

        # Логи
        self.check('LOGGING', 'None', 'LOGGING должен быть настроен для отслеживания ошибок.', check_type="exists")

        # Дополнительные проверки
        self.check('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True', 'SECURE_HSTS_INCLUDE_SUBDOMAINS должен быть включен для защиты поддоменов.')
        self.check('SECURE_HSTS_PRELOAD', 'True', 'SECURE_HSTS_PRELOAD должен быть включен для добавления домена в список preload.')

        return self.issues


class FlaskConfigAudit(ConfigAuditStrategy):
    """Стратегия аудита для Flask."""

    def run_audit(self):
        # Отладка
        self.check('DEBUG', 'False', 'DEBUG должен быть отключен в продакшене.')

        # Безопасность
        self.check('SECRET_KEY', 'None', 'SECRET_KEY должен быть установлен и не быть значением по умолчанию.', check_type="not_equal")
        self.check('SESSION_COOKIE_SECURE', 'True', 'SESSION_COOKIE_SECURE должен быть включен для HTTPS.')
        self.check('SESSION_COOKIE_HTTPONLY', 'True', 'SESSION_COOKIE_HTTPONLY должен быть включен для защиты cookie от JavaScript.')
        self.check('SESSION_COOKIE_SAMESITE', 'Strict', 'SESSION_COOKIE_SAMESITE должен быть установлен в "Strict" или "Lax".')
        self.check('PREFERRED_URL_SCHEME', 'https', 'PREFERRED_URL_SCHEME должен быть установлен в "https".')

        # Логи
        self.check('LOGGING_CONFIG', 'None', 'LOGGING_CONFIG должен быть настроен для отслеживания ошибок.', check_type="exists")

        # Заголовки
        self.check('APPLICATION_ROOT', '/', 'APPLICATION_ROOT должен быть корректно установлен для маршрутизации.')

        return self.issues


class ConfigAuditor:
    """Класс аудита конфигурации, использующий паттерн "Стратегия"."""

    def __init__(self, strategy):
        self.strategy = strategy

    def audit(self):
        return self.strategy.run_audit()


# Пример использования для Django
django_settings = {
    'DEBUG': True,
    'SECRET_KEY': 'default',
    'ALLOWED_HOSTS': ['*'],
    'SECURE_SSL_REDIRECT': False,
    'CSRF_COOKIE_SECURE': False,
    'SESSION_COOKIE_SECURE': False,
    'SECURE_HSTS_SECONDS': 0,
    'LOGGING': None,
}
