import pytest
import requests
import json

import Config
from src import AdditionalFunctions as AF
from src.pydantics import subscriptions_data as SD
from src.pydantics import current_data as CD

url_subscriptions = "https://api.vkplay.live/v1/user/public_video_stream/subscriptions"
url_current = "https://api.vkplay.live/v1/user/current"


def GetResponse(url):
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {AF.GetCookieToken()}'
    }
    return requests.request(
        "GET", url, headers=headers, data=payload)


class TestAPI:

    def test_api_subscriptions(self):
        '''401 | Проверка схемы запроса со списком подписок'''

        response = GetResponse(url_subscriptions)

        if response.status_code == 200:
            SD.Response.model_validate(json.loads(response.text))
        else:
            pytest.fail("Статус код ответа не 200")

        # print(headers)
        # print(response.text)

    def test_api_current(self):
        '''402 | Проверка схемы запроса с данными пользователя'''

        response = GetResponse(url_current)

        if response.status_code == 200:
            CD.Response.model_validate(json.loads(response.text))
            assert dict(json.loads(response.text))[
                "displayName"] == Config.USERNAME
        else:
            pytest.fail("Статус код ответа не 200")
