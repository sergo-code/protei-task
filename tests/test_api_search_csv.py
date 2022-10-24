import allure
import pytest

from utils.csv_reader import get_data
from utils.json_util import validate_json_schema


@allure.epic('API тесты')
@allure.description("Проверка соответствия адреса и координат")
@pytest.mark.parametrize('item', get_data('data.csv'))
class TestNominatimSearch:
    @allure.feature("/search")
    @allure.story("Проверить корректность координат для заданного адреса")
    def test_search(self, nominatim_api, item):
        params = {
            "q": item[0],
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
                if item[1] == obj['place_id']:
                    with allure.step(f"Ответ содержит корректную координату lat"):
                        assert item[2] == obj['lat']
                    with allure.step(f"Ответ содержит корректную координату lon"):
                        assert item[3] == obj['lon']
                    break

    @allure.feature("/reverse")
    @allure.story("Проверить корректность адреса для заданных координат")
    def test_search_reverse(self, nominatim_api, item):
        params = {
            "lat": item[2],
            "lon": item[3],
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
            assert int(item[1]) == response.json()['place_id']

        address = item[0].split()
        temp = 0
        for value in response.json()['address'].values():
            temp_value = value.lower().split(' ')
            for i in temp_value:
                for temp_address in address:
                    if temp_address.lower() in i:
                        temp += 1

        with allure.step(f"Заданный адрес совпадает с адресом по заданным координатам"):
            assert len(address) <= temp
