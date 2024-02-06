from enum import StrEnum

import requests


class MapType(StrEnum):
    SCHEMA = 'map'
    SATELLITE = 'sat'
    HYBRID = 'hyb'


class MapImage:
    def __init__(self) -> None:
        self._longitude: float = 37.530887
        self._latitude: float = 55.70311
        self._scale: float = 0.002
        self._type: MapType = MapType.SCHEMA

    @property
    def image(self) -> bytes or None:
        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return None
        return response.content
