import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from ticker.models import Ticker 

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_data():
    now = datetime.now()
    return [
        Ticker.objects.create(
            symbol='BTC',
            price=50000.50,
            timestamp=now - timedelta(hours=2)
        ),
        Ticker.objects.create(
            symbol='BTC',
            price=51000.75,
            timestamp=now - timedelta(hours=1)
        ),
        Ticker.objects.create(
            symbol='ETH',
            price=3000.25,
            timestamp=now
        )
    ]

# Тест базового доступа к эндпоинту
@pytest.mark.django_db
def test_ticker_list_basic(api_client, test_data):
    url = reverse('ticker-list')  
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3 

# Тест фильтрации по symbol
@pytest.mark.django_db
def test_filter_by_symbol(api_client, test_data):
    url = reverse('ticker-list')
    response = api_client.get(url, {'symbol': 'BTC'})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert all(item['symbol'] == 'BTC' for item in response.data)

# Тест фильтрации по timestamp 
@pytest.mark.django_db
def test_filter_by_timestamp(api_client, test_data):
    target_timestamp = test_data[0].timestamp.isoformat()
    url = reverse('ticker-list')
    response = api_client.get(url, {'timestamp': target_timestamp})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['symbol'] == 'BTC'


# Тест пустого результата
@pytest.mark.django_db
def test_empty_filter_result(api_client, test_data):
    url = reverse('ticker-list')
    response = api_client.get(url, {'symbol': 'XRP'})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

# Тест частичной фильтрации по дате
@pytest.mark.django_db
def test_date_part_filter(api_client, test_data):
    target_date = test_data[0].timestamp.date().isoformat()
    url = reverse('ticker-list')
    response = api_client.get(url, {'timestamp__date': target_date})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1 