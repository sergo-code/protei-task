import pytest

from api.nominatim import NominatimAPI


@pytest.fixture(scope='session')
def nominatim_api():
    return NominatimAPI()
