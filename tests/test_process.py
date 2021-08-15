import pytest
import asyncio
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



