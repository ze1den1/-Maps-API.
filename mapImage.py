from enum import StrEnum

import requests


class MapType(StrEnum):
    SCHEMA = 'map'
    SATELLITE = 'sat'
    HYBRID = 'hyb'


class MapImage:
    SCALE_MAX = 35
    SCALE_MIN = 0.000125
    API = 'http://static-maps.yandex.ru/1.x/'

    def __init__(self) -> None:
        self._longitude: float = 37.530887
        self._latitude: float = 55.70311
        self._scale: float = 0.002
        self._type: MapType = MapType.SCHEMA

    @property
    def image(self) -> bytes or None:
        params = {
            'll': ','.join(map(str, (self._longitude, self._latitude))),
            'spn': ','.join(map(str, (self._scale, self._scale))),
            'l': self._type
        }
        response = requests.get(self.API, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return None
        return response.content

    def scaling(self, coeff: float) -> None:
        scale = self._scale * coeff
        if self.SCALE_MIN <= scale <= self.SCALE_MAX:
            self._scale = scale

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        if not (-180.0 <= value <= 180.0):
            value += 180.0
            value %= 360.0
            value -= 180.0
        self._longitude = value

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        if -90.0 <= value <= 90.0:
            self._latitude = value

    def move(self, d_longitude: float, d_latitude: float) -> None:
        self.longitude += d_longitude
        self._latitude += d_latitude

    def screen_up(self) -> None:
        self.move(0, self._scale)

    def screen_down(self) -> None:
        self.move(0, -self._scale)

    def screen_left(self) -> None:
        self.move(-self._scale, 0)

    def screen_right(self) -> None:
        self.move(self._scale, 0)
