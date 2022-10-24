import allure
import pytest

from utils.json_reader import get_data
from utils.json_util import validate_json_schema


@allure.epic('API тесты')
@allure.description("Проверка соответствия адреса и координат")
@pytest.mark.parametrize('item', get_data('data.json'))
class TestNominatimSearch:
    @allure.feature("/search")
    @allure.story("Проверить корректность координат для заданного адреса")
    def test_search(self, nominatim_api, item):
        params = {
            "q": item[1],
            "polygon_geojson": 1,
            "format": "jsonv2"
        }
        with allure.step(f"Отправка запроса GET /search"):
            response = nominatim_api.search(params)
        with allure.step(f"Статус код успешный (200)"):
            assert response.status_code == 200
        with allure.step(f"Ответ содержит всю информацию по шаблону"):
            validate_json_schema(response.json(), 'get_search')

        with allure.step(f"Ответ содержит необходимый тип объекта"):
            for obj in response.json():
                if item[0] == obj['place_id']:
                    with allure.step(f"Ответ содержит корректную координату lat"):
                        assert item[3]['lat'] == obj['lat']
                    with allure.step(f"Ответ содержит корректную координату lon"):
                        assert item[3]['lon'] == obj['lon']
                    break

    @allure.feature("/reverse")
    @allure.story("Проверить корректность адреса для заданных координат")
    def test_search_reverse(self, nominatim_api, item):
        params = {
            "lat": item[3]['lat'],
            "lon": item[3]['lon'],
            "zoom": 18,
            "format": "jsonv2"
        }
        with allure.step(f"Отправка запроса GET /reverse"):
            response = nominatim_api.reverse(params)
        with allure.step(f"Статус код успешный (200)"):
            assert response.status_code == 200
        with allure.step(f"Ответ содержит всю информацию по шаблону"):
            validate_json_schema(response.json(), 'get_search_reverse')
        with allure.step(f"Ответ содержит необходимый тип объекта"):
            assert item[0] == response.json()['place_id']
        with allure.step(f"Заданный адрес совпадает с адресом по заданным координатам"):
            assert item[2] == response.json()['address']
