import io
from enum import StrEnum
from PIL import Image
import requests


class MapType(StrEnum):
    SCHEMA = 'map'
    SATELLITE = 'sat'
    HYBRID = 'skl'


class MapImage:
    SCALE_MAX = 35
    SCALE_MIN = 0.000125
    API = 'http://static-maps.yandex.ru/1.x/'

    def __init__(self) -> None:
        self._longitude: float = 37.530887
        self._latitude: float = 55.70311
        self._scale: float = 0.002
        self._type: MapType = MapType.SCHEMA

    def _get_image(self, _type: MapType) -> bytes or None:
        params = {
            'll': ','.join(map(str, (self._longitude, self._latitude))),
            'spn': ','.join(map(str, (self._scale, self._scale))),
            'l': _type
        }
        response = requests.get(self.API, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return None
        return response.content

    @property
    def image(self) -> bytes or None:
        if self._type != MapType.HYBRID:
            return self._get_image(self._type)
        satellite_image = Image.open(io.BytesIO(self._get_image(MapType.SATELLITE)))
        hybrid_mask = Image.open(io.BytesIO(self._get_image(MapType.HYBRID)))
        satellite_image.paste(hybrid_mask, (0, 0), hybrid_mask)
        im_byte_arr = io.BytesIO()
        satellite_image.save(im_byte_arr, format='PNG')
        return im_byte_arr.getvalue()

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

    def set_type(self, _type):
        self._type = _type
