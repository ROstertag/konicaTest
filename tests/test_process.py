import pytest
import asyncio
from asyncmock import AsyncMock
from nats.aio.client import Client
from processor.process import convert_rgb_to_names
from processor.process import run
from mock import patch, Mock

@pytest.mark.parametrize("colors", [
        ((123,23,23), 'maroon'),
        ((123,123,123), 'grey'),
        ((123,3,123), 'purple'),
        ((223,123,13), 'chocolate'),
        ((53,33,13), 'black'),
    ])
def test_convert_rgb_to_names(colors):
    result = convert_rgb_to_names(colors[0])
    assert result == colors[1]


# monkey patch MagicMock
async def async_magic():
    pass

Mock.__await__ = lambda x: async_magic().__await__()


@patch('processor.process.Client')
def test_run(mock_nats_client):
    mock_nats_client.subscribe.return_value = 123
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()

