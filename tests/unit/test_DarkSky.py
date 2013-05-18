import mock
from nose.tools import assert_equals, assert_raises
from darksky import DarkSky
from darksky import DarkSkyException
import json
import datetime

def test_getWeather_success():
    mock_http = mock.Mock()
    mock_dsresponse = mock.Mock()
    mock_dsresponse.return_value = "something"
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http,
        DarkSkyResponseClass=mock_dsresponse
    )
    mock_http.open.return_value = (
        200,
        json.dumps(
            {"data": True}
        )
    )
    ret_val = instance.getWeather(latitude=123, longitude=1234)
    
    yield (
        assert_equals,
        "something",
        ret_val
    )

    yield (
        assert_equals,
        "https://api.forecast.io/forecast/abc/123,1234",
        mock_http.open.call_args[1]["url"]
    )

    yield (
        assert_equals,
        {"data": True},
        mock_dsresponse.call_args[1]["response_body"]
    )

    yield (
        assert_equals,
        "brief",
        mock_dsresponse.call_args[1]["forecast_type"]
    )

def test_getWeather_failure():
    mock_http = mock.Mock()
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http
    )
    mock_http.open.return_value = (
        403,
        json.dumps(
            {
                "code": 403,
                "error": "Forbidden"
            }
        )
    )
    yield (
        assert_raises,
        DarkSkyException,
        instance.getWeather,
        123,
        1234,
        "brief"
    )

def test_getInteresting():
    mock_http = mock.Mock()
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http
    )
    mock_http.open.return_value = (
        200,
        json.dumps(
            {
                "storms": {
                    "data": True
                }
            }
        )
    )

    yield (
        assert_equals,
        True,
        instance.getInteresting()["data"]
    )
    
    yield (
        assert_equals,
        "https://api.darkskyapp.com/v1/interesting/abc",
        mock_http.open.call_args[1]["url"]
    )

def test_getInteresting_failure():
    mock_http = mock.Mock()
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http
    )
    mock_http.open.return_value = (
        403,
        json.dumps(
            {
                "code": 403,
                "error": "Forbidden"
            }
        )
    )
    yield (
        assert_raises,
        DarkSkyException,
        instance.getInteresting
    )

def test_getWeathers():
    mock_http = mock.Mock()
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http
    )
    mock_http.open.return_value = (
        200,
        json.dumps(
            {
              "precipitation": [
                { "probability": 1.0,
                  "intensity": 15.6,
                  "error": 1.0,
                  "type": "rain",
                  "time": 1325607100 },
                { "probability": 0.0,
                  "intensity": 0.0,
                  "error": 0.0,
                  "type": "rain",
                  "time": 1325607791 }
              ]
            }
        )
    )
    time1 = datetime.datetime(
        year=1999,
        month=12,
        day=1
    )
    time2 = datetime.datetime(
        year=1995,
        month=12,
        day=1,
    )
    ret = instance.getWeathers(
        [
            {
                "latitude": 12345.11,
                "longitude": 12345.12,
                "time": time1
            },
            {
                "latitude": 12345.13,
                "longitude": 12345.14,
                "time": time2
            }
        ]
    )
    yield (
        assert_equals,
        15.6,
        ret[0]["intensity"]
    )
    yield (
        assert_equals,
        0,
        ret[1]["intensity"]
    )
    yield (
        assert_equals,
        "https://api.darkskyapp.com/v1/precipitation/abc/12345.11,12345.12,944006400;12345.13,12345.14,817776000",
        mock_http.open.call_args[1]["url"]
    )
