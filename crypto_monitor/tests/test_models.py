import pytest
from django.db import models
from decimal import Decimal
from django.utils import timezone
from ticker.models import Ticker  

def test_ticker_model_fields():
    # Проверка поля 'symbol'
    symbol_field = Ticker._meta.get_field('symbol')
    assert isinstance(symbol_field, models.CharField)
    assert symbol_field.max_length == 10

    # Проверка поля 'price'
    price_field = Ticker._meta.get_field('price')
    assert isinstance(price_field, models.DecimalField)
    assert price_field.max_digits == 20
    assert price_field.decimal_places == 8

    # Проверка поля 'timestamp'
    timestamp_field = Ticker._meta.get_field('timestamp')
    assert isinstance(timestamp_field, models.DateTimeField)
    assert timestamp_field.auto_now_add is True

# Тестирование создания объекта и сохранения в БД
@pytest.mark.django_db
def test_create_ticker():
    ticker = Ticker.objects.create(
        symbol='BTC',
        price=Decimal('50000.12345678')
    )
    assert ticker.symbol == 'BTC'
    assert ticker.price == Decimal('50000.12345678')
    assert ticker.timestamp is not None

# Тестирование строкового представления объекта
@pytest.mark.django_db
def test_ticker_str_method():
    ticker = Ticker.objects.create(
        symbol='BTC',
        price=Decimal('50000.12345678')
    )
    expected_str = f"{ticker.symbol} {ticker.price} at {ticker.timestamp}"
    assert str(ticker) == expected_str

# Проверка автоматического добавления временной метки
@pytest.mark.django_db
def test_timestamp_auto_now_add():
    before_creation = timezone.now()
    ticker = Ticker.objects.create(symbol='ETH', price=Decimal('3000.5'))
    after_creation = timezone.now()
    assert ticker.timestamp >= before_creation
    assert ticker.timestamp <= after_creation

# Проверка, что временная метка не обновляется при сохранении
@pytest.mark.django_db
def test_timestamp_not_updated_on_save():
    ticker = Ticker.objects.create(symbol='ETH', price=Decimal('3000.5'))
    original_timestamp = ticker.timestamp
    ticker.price = Decimal('4000.0')
    ticker.save()
    ticker.refresh_from_db()
    assert ticker.timestamp == original_timestamp