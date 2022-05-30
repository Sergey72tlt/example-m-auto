import datetime
from django.core.exceptions import ValidationError


def validate_birth_date(value):
    """Проверяет корректность даты рождения."""
    if value >= datetime.datetime.now().date():
        raise ValidationError(f'Дата рождения не может быть больше текущей даты.')
