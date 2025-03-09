import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from crypto_monitor.routing import application  


# Тестовое подключение и добавление в группу
@pytest.mark.asyncio
async def test_connect_and_group_add():
    communicator = WebsocketCommunicator(application, "/ws/tickers/")
    
    connected, _ = await communicator.connect()
    assert connected
    
    channel_layer = get_channel_layer()
    test_data = {"price": 100}
    await channel_layer.group_send(
        "tickers",
        {
            "type": "send_ticker",
            "data": test_data
        }
    )

    response = await communicator.receive_json_from()
    assert response == test_data
    
    await communicator.disconnect()


# Тестовое отключение и групповой сброс
@pytest.mark.asyncio
async def test_disconnect_and_group_discard():
    communicator = WebsocketCommunicator(application, "/ws/tickers/")
    await communicator.connect()
    
    await communicator.disconnect()
    
    channel_layer = get_channel_layer()
    await channel_layer.group_send("tickers", {"type": "send_ticker", "data": {"price": 100}})
    
    with pytest.raises(Exception):
        await communicator.receive_json_from() 
